"""The pinned bd installation routes and the wrapper that dispatches them.

Three subjects, one contract (bead coding-harness-tr84, change bd-1-3-4): the
repository wrapper `tools/bd` dispatches only the pinned versioned binary and
refuses the schema verbs; the repository installer `tools/beads/install.sh` and
the standalone cloud setup `tools/cloud-env/setup.sh` download the pinned
release from the canonical gastownhall/beads repository and install it only
after the archive matches the committed checksum. Nothing here touches a real
tracker, home or binary: every case copies the real scripts into a disposable
repository layout, runs them under a temporary HOME with a fully controlled
PATH, and lets a recording curl stand-in serve local fixture tarballs whose
hashes are computed in this file — never inferred from a version string.

Criterion numbers cite the plan's `## Criterion ledger` of change bd-1-3-4.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
WRAPPER = REPO_ROOT / "tools" / "bd"
INSTALLER = REPO_ROOT / "tools" / "beads" / "install.sh"
SETUP = REPO_ROOT / "tools" / "cloud-env" / "setup.sh"
VERSION_FILE = REPO_ROOT / "tools" / "beads" / "VERSION"
SHIM = REPO_ROOT / "tools" / "beads" / "bin" / "bd"
BASH = shutil.which("bash") or "/bin/bash"

# The externals the three scripts under test call. Every one of them is
# symlinked from the host into the controlled bin directory — so no host `bd`
# (the maintainer's global guard included) can ever be found by a run.
TOOLS = (
    "tr",
    "dirname",
    "head",
    "grep",
    "awk",
    "find",
    "mktemp",
    "rm",
    "mkdir",
    "install",
    "cat",
    "chmod",
    "env",
    "sh",
    "bash",
    # GNU tar (the Linux runner) execs gzip for `tar -xzf`; bsdtar (macOS)
    # links zlib and does not. The installer needs it, so the PATH carries it.
    "gzip",
)

FAKE_BD = """#!/bin/bash
# Recording stand-in for a real bd binary (test fixture): reports a fixed
# version, logs every invocation argument-per-line, and exits BD_RC for any
# command other than `version`.
log="@LOG@"
printf 'CALL\\n' >>"$log"
for argument in "$@"; do
  printf 'ARG<%s>\\n' "$argument" >>"$log"
done
if [ "${1:-}" = version ]; then
  printf 'bd version @VERSION@ (fixture)\\n'
  exit 0
fi
exit "${BD_RC:-0}"
"""

CURL_STUB = """#!/bin/bash
# Recording stand-in for curl (test fixture): logs every requested URL and,
# when CURL_SERVE names a file, serves its bytes as the -o target.
url=""
target=""
while [ $# -gt 0 ]; do
  case "$1" in
    -o) target="$2"; shift 2 ;;
    -*) shift ;;
    *) url="$1"; shift ;;
  esac
done
printf '%s\\n' "$url" >>"${CURL_LOG:?}"
if [ -n "${CURL_SERVE:-}" ]; then
  cat "${CURL_SERVE}" >"$target" || exit 1
fi
exit "${CURL_RC:-0}"
"""

UNAME_STUB = """#!/bin/bash
# Platform stand-in for uname (test fixture): UNAME_S answers -s, UNAME_M -m.
case "${1:-}" in
  -m) printf '%s\\n' "${UNAME_M:?}" ;;
  *) printf '%s\\n' "${UNAME_S:?}" ;;
esac
"""

HASH_SHIM = """#!/bin/bash
# Portable sha256 stand-in (test fixture): prints "<hex>  <path>" like the
# coreutils and Perl tools, so the scripts' awk '{print $1}' reads the digest
# regardless of the host. Serves as shasum and as sha256sum alike.
exec python3 -c 'import hashlib, sys
paths = []
skip_value = False
for argument in sys.argv[1:]:
    if skip_value:
        skip_value = False
    elif argument == "-a":
        skip_value = True
    elif not argument.startswith("-"):
        paths.append(argument)
for path in paths:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    print(digest.hexdigest() + "  " + path)' "$@"
"""

TAR_STUB = """#!/bin/bash
# Recording stand-in for tar (test fixture): logs every invocation, then runs
# the host's real tar, so extraction itself stays real and observable.
printf '%s\\n' "$*" >>"${TAR_LOG:?}"
exec "@TAR@" "$@"
"""

NEUTRAL_STUB = """#!/bin/bash
# Neutral stand-in for an unrelated cloud command, uv and git alike (test
# fixture): logs its arguments and succeeds, so a broken /home/user redirect
# can never reach the host's real tool.
printf '%s\\n' "$*" >>"${NEUTRAL_LOG:?}"
exit 0
"""

SHIM_COPY = """#!/usr/bin/env sh
# Recording copy of the repository PATH shim (test fixture): logs one line,
# then forwards exactly like the real shim — so a wrapper that accepted this
# shim would recurse into itself and never terminate.
printf 'CALL\\n' >>"@LOG@"
here="$(cd "$(dirname "$0")" && pwd)"
exec "$here/../../bd" "$@"
"""

# Host environment variables that could leak into a run and decide its outcome.
STRIPPED_ENV = (
    "BD_PIN_BYPASS",
    "BD_RC",
    "BD_LOG",
    "CURL_LOG",
    "CURL_SERVE",
    "CURL_RC",
    "UNAME_S",
    "UNAME_M",
    "NEUTRAL_LOG",
    "TAR_LOG",
)

ROUTES = [
    ("installer", "Darwin", "arm64"),
    ("installer", "Linux", "amd64"),
    ("cloud", "Linux", "amd64"),
]

# No skip: neither this file nor tools/ travels with the kit (scripts/kit/manifest.yaml, both
# `bestand`), so a missing wrapper, installer, shim, pin or cloud setup fails these tests loudly
# instead of silently skipping the guards (loop row L1-3 of change bd-1-3-4).


def _pin() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def _sandbox(tmp_path: Path, *, name: str = "repo") -> SimpleNamespace:
    """A disposable repository layout: the real wrapper, installer, shim and
    pin copied verbatim, an empty checksums directory, an empty HOME beside."""
    repo = tmp_path / name
    tools = repo / "tools"
    (tools / "beads" / "checksums").mkdir(parents=True)
    (tools / "beads" / "bin").mkdir(parents=True)
    for source, target in (
        (WRAPPER, tools / "bd"),
        (INSTALLER, tools / "beads" / "install.sh"),
        (SHIM, tools / "beads" / "bin" / "bd"),
    ):
        target.write_bytes(source.read_bytes())
        target.chmod(0o755)
    (tools / "beads" / "VERSION").write_text(_pin() + "\n", encoding="utf-8")
    home = tmp_path / f"home-{name}"
    home.mkdir()
    return SimpleNamespace(
        repo=repo,
        home=home,
        checksums=tools / "beads" / "checksums",
        versioned=home / ".local" / "bin" / f"bd-{_pin()}",
    )


def _path_bin(tmp_path: Path, *, name: str = "pathbin") -> Path:
    """A fully controlled PATH directory: the external tools the scripts need,
    python3 for the hash shims, the shims themselves, the recording curl and
    platform uname stubs, neutral uv/git stubs — but no bd."""
    bin_dir = tmp_path / name
    bin_dir.mkdir()
    for tool in TOOLS:
        found = shutil.which(tool)
        assert found, f"{tool} is missing — a controlled PATH cannot be built here"
        (bin_dir / tool).symlink_to(found)
    (bin_dir / "python3").symlink_to(sys.executable)
    for tool in ("shasum", "sha256sum"):
        shim = bin_dir / tool
        shim.write_text(HASH_SHIM, encoding="utf-8")
        shim.chmod(0o755)
    for tool in ("uv", "git"):
        stub = bin_dir / tool
        stub.write_text(NEUTRAL_STUB, encoding="utf-8")
        stub.chmod(0o755)
    real_tar = shutil.which("tar")
    assert real_tar, "tar is missing — a controlled PATH cannot be built here"
    tar_stub = TAR_STUB.replace("@TAR@", real_tar)
    for tool, stub_text in (("curl", CURL_STUB), ("uname", UNAME_STUB), ("tar", tar_stub)):
        stub = bin_dir / tool
        stub.write_text(stub_text, encoding="utf-8")
        stub.chmod(0o755)
    return bin_dir


def _path(*parts: Path | str) -> str:
    return os.pathsep.join(str(part) for part in parts)


def _fake_bd(path: Path, *, version: str, log: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FAKE_BD.replace("@LOG@", str(log)).replace("@VERSION@", version), encoding="utf-8")
    path.chmod(0o755)


def _log_lines(log: Path) -> list[str]:
    if not log.exists():
        return []
    return log.read_text(encoding="utf-8").splitlines()


def _calls(log: Path) -> list[list[str]]:
    """The invocations a fake bd recorded, one argument list per call."""
    calls: list[list[str]] = []
    for line in _log_lines(log):
        if line == "CALL":
            calls.append([])
        elif line.startswith("ARG<") and line.endswith(">"):
            calls[-1].append(line[4:-1])
    return calls


def _bd_tarball(tmp_path: Path, *, name: str, version: str) -> tuple[Path, str]:
    """A real gzip tarball holding an executable `bd` that reports `version`;
    returns the archive path and its actual sha256 digest."""
    build = tmp_path / f"build-{name}"
    build.mkdir()
    inside = build / "bd"
    _fake_bd(inside, version=version, log=tmp_path / f"log-{name}.log")
    archive = tmp_path / f"{name}.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(inside, arcname="bd")
    return archive, hashlib.sha256(archive.read_bytes()).hexdigest()


def _checksum_file(sandbox: SimpleNamespace, tarball: str, digest: str) -> Path:
    sums = sandbox.checksums / f"{tarball}.sha256"
    sums.write_text(digest + "\n", encoding="utf-8")
    return sums


def _sentinel(home: Path) -> Path:
    """The unversioned bd path: a global bd another repository may need —
    neither installation route may ever touch it."""
    sentinel = home / ".local" / "bin" / "bd"
    sentinel.parent.mkdir(parents=True, exist_ok=True)
    sentinel.write_text("sentinel: a global bd another repository depends on\n", encoding="utf-8")
    return sentinel


def _cloud_copy(tmp_path: Path, *, root: Path, digest: str | None = None) -> Path:
    """A copy of the real cloud setup with `/home/user` redirected into an
    empty temporary root and, when given, the BD_SHA256 literal replaced —
    both changes to the test copy only, never to the tracked script."""
    text = SETUP.read_text(encoding="utf-8").replace("/home/user", str(root))
    if digest is not None:
        text = re.sub(r"^BD_SHA256=([0-9a-f]{64})", f"BD_SHA256={digest}", text, count=1, flags=re.M)
    copy = tmp_path / "cloud-setup.sh"
    copy.write_text(text, encoding="utf-8")
    copy.chmod(0o755)
    return copy


def _run(
    script: Path,
    *,
    home: Path,
    path: str,
    env_extra: dict[str, str] | None = None,
    args: list[str] | None = None,
) -> subprocess.CompletedProcess[str]:
    env = {key: value for key, value in os.environ.items() if key not in STRIPPED_ENV}
    env["HOME"] = str(home)
    env["PATH"] = path
    env["TAR_LOG"] = str(home.parent / f"tar-{home.name}.log")
    if env_extra:
        env.update(env_extra)
    # The host bash by absolute path: the controlled PATH of a run must not
    # decide which interpreter starts the script under test.
    return subprocess.run(
        [BASH, str(script), *(args or [])],
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def _extractions(home: Path) -> list[str]:
    """The tar invocations a run under this HOME made (the recording tar stand-in's log)."""
    return _log_lines(home.parent / f"tar-{home.name}.log")


def _assert_installed(home: Path, pin: str, sentinel: Path) -> None:
    dest = home / ".local" / "bin" / f"bd-{pin}"
    assert dest.is_file(), f"no versioned binary was installed at {dest}"
    assert os.access(dest, os.X_OK), f"the installed binary at {dest} is not executable"
    check = subprocess.run([str(dest), "version"], capture_output=True, text=True, timeout=60, check=False)
    assert check.returncode == 0, check.stderr
    assert f"bd version {pin}" in check.stdout, f"the installed binary reports {check.stdout!r}"
    assert sentinel.read_text(encoding="utf-8").startswith("sentinel:"), "the unversioned bd path was overwritten"


def test_wrapper_selects_pinned_versioned_binary(tmp_path: Path) -> None:
    """Criterion 1: with the pinned versioned binary installed, the wrapper
    dispatches it ahead of any bd on PATH, passes the command's arguments
    boundary-per-boundary, and preserves the child's exit status."""
    pin = _pin()
    ns = _sandbox(tmp_path)
    pinned_log = tmp_path / "pinned-bd.log"
    _fake_bd(ns.versioned, version=pin, log=pinned_log)
    path_log = tmp_path / "path-bd.log"
    bd_dir = tmp_path / "bd-on-path"
    _fake_bd(bd_dir / "bd", version="9.9.9", log=path_log)
    path = _path(bd_dir, _path_bin(tmp_path))
    result = _run(
        ns.repo / "tools" / "bd",
        home=ns.home,
        path=path,
        env_extra={"BD_RC": "3"},
        args=["ready", "--json"],
    )
    assert result.returncode == 3, (result.stdout, result.stderr)
    assert result.stderr == "", "a successful dispatch must stay quiet"
    assert _calls(pinned_log) == [["version"], ["ready", "--json"]], (
        "the pinned binary must probe its own version and then receive the command, arguments intact"
    )
    assert _calls(path_log) == [], "a bd on PATH was dispatched although the pinned binary is installed"


@pytest.mark.parametrize(
    "reported_version", ["1.3.0", "9.9.9", *(_pin() + suffix for suffix in ("-rc.1", "+build.1", ".0", "0", "x"))]
)
@pytest.mark.parametrize(
    ("installed", "bypass", "command"),
    [
        ("versioned-binary", False, ["ready"]),
        ("path-binary", False, ["ready"]),
        ("versioned-binary", True, ["ready"]),
        ("path-binary", True, ["ready"]),
        ("versioned-binary", True, ["migrate"]),
    ],
)
def test_wrapper_refuses_version_mismatch(
    tmp_path: Path, installed: str, bypass: bool, command: list[str], reported_version: str
) -> None:
    """Criterion 5: a binary reporting any version other than the pin is never
    dispatched — not the versioned one, not the one on PATH, and not even when
    BD_PIN_BYPASS=1 is set, for a normal command (the criterion's refuting
    case, loop row L1-7) as for the blocked verbs' escape hatch."""
    ns = _sandbox(tmp_path)
    log = tmp_path / "mismatching-bd.log"
    extra: dict[str, str] = {}
    if installed == "versioned-binary":
        _fake_bd(ns.versioned, version=reported_version, log=log)
        path = _path(_path_bin(tmp_path))
    else:
        bd_dir = tmp_path / "bd-on-path"
        _fake_bd(bd_dir / "bd", version=reported_version, log=log)
        path = _path(bd_dir, _path_bin(tmp_path))
    if bypass:
        extra["BD_PIN_BYPASS"] = "1"
    result = _run(ns.repo / "tools" / "bd", home=ns.home, path=path, env_extra=extra, args=command)
    assert result.returncode != 0, f"a mismatching bd was dispatched: {command}"
    assert "version mismatch" in result.stderr, result.stderr
    assert _calls(log) == [["version"]], "only the version probe may reach a mismatching binary, never the command"


def test_wrapper_falls_back_to_a_matching_path_binary(tmp_path: Path) -> None:
    """Criterion 1, fallback side (loop row L1-11): with no versioned binary
    installed, a bd on PATH that reports the pin is dispatched — the path a
    machine without `~/.local/bin/bd-<pin>` takes — with its arguments and
    exit status intact."""
    pin = _pin()
    ns = _sandbox(tmp_path)
    path_log = tmp_path / "path-bd.log"
    bd_dir = tmp_path / "bd-on-path"
    _fake_bd(bd_dir / "bd", version=pin, log=path_log)
    assert not ns.versioned.exists()
    result = _run(
        ns.repo / "tools" / "bd",
        home=ns.home,
        path=_path(bd_dir, _path_bin(tmp_path)),
        env_extra={"BD_RC": "5"},
        args=["show", "id with space"],
    )
    assert result.returncode == 5, (result.stdout, result.stderr)
    assert _calls(path_log) == [["version"], ["show", "id with space"]], (
        "the pin-matching bd on PATH must probe its version and then receive the command, arguments intact"
    )


@pytest.mark.parametrize("verb", ["init", "migrate", "upgrade"])
def test_wrapper_blocks_schema_verbs(tmp_path: Path, verb: str) -> None:
    """Criterion 6: init, migrate and upgrade never reach the binary without
    BD_PIN_BYPASS=1 — while the explicit bypass still unlocks them, so the
    refusal is the verb gate and not a broken wrapper."""
    pin = _pin()
    ns = _sandbox(tmp_path)
    path = _path(_path_bin(tmp_path))
    blocked_log = tmp_path / f"blocked-{verb}.log"
    _fake_bd(ns.versioned, version=pin, log=blocked_log)
    blocked = _run(ns.repo / "tools" / "bd", home=ns.home, path=path, args=[verb])
    assert blocked.returncode != 0, f"{verb} was dispatched without the bypass"
    assert "blocked by tools/bd" in blocked.stderr, blocked.stderr
    assert _calls(blocked_log) == [["version"]], f"the {verb} command reached the binary without the bypass"

    bypassed_log = tmp_path / f"bypassed-{verb}.log"
    _fake_bd(ns.versioned, version=pin, log=bypassed_log)
    bypassed = _run(ns.repo / "tools" / "bd", home=ns.home, path=path, env_extra={"BD_PIN_BYPASS": "1"}, args=[verb])
    assert bypassed.returncode == 0, bypassed.stderr
    assert _calls(bypassed_log) == [["version"], [verb]], "the explicit bypass must still unlock the blocked verb"


def test_wrapper_missing_binary_exits_127(tmp_path: Path) -> None:
    """Criterion 7: with no eligible bd anywhere, the wrapper exits exactly
    127 — and it does not take the repository's own PATH shim, which forwards
    back into the wrapper and would recurse forever."""
    ns = _sandbox(tmp_path)
    bin_dir = _path_bin(tmp_path)
    missing = _run(ns.repo / "tools" / "bd", home=ns.home, path=_path(bin_dir), args=["ready"])
    assert missing.returncode == 127, f"the missing-binary exit status is {missing.returncode}, not 127"
    assert "no bd binary found" in missing.stderr, missing.stderr

    # The hook shim inside this repository must never be taken as the binary.
    # The recording copy leaves a log line if it is ever executed.
    shim_log = tmp_path / "shim.log"
    shim = ns.repo / "tools" / "beads" / "bin" / "bd"
    shim.write_text(SHIM_COPY.replace("@LOG@", str(shim_log)), encoding="utf-8")
    shim.chmod(0o755)
    looped = _run(
        ns.repo / "tools" / "bd",
        home=ns.home,
        path=_path(ns.repo / "tools" / "beads" / "bin", bin_dir),
        args=["ready"],
    )
    assert looped.returncode == 127, f"the repository shim was accepted as the binary: {looped.returncode}"
    assert not shim_log.exists(), "the repository's PATH shim was executed by the wrapper"


@pytest.mark.parametrize(("route", "os_name", "arch"), ROUTES)
def test_install_routes_request_canonical_release(tmp_path: Path, route: str, os_name: str, arch: str) -> None:
    """Criterion 2: whichever route downloads bd asks the canonical
    gastownhall/beads release for exactly the pinned platform archive — the
    old owner, another version or another host fails here."""
    pin = _pin()
    tarball = f"beads_{pin}_{os_name.lower()}_{arch}.tar.gz"
    expected = f"https://github.com/gastownhall/beads/releases/download/v{pin}/{tarball}"
    archive, _ = _bd_tarball(tmp_path, name=f"request-{route}-{arch}", version=pin)
    curl_log = tmp_path / "curl.log"
    neutral_log = tmp_path / "neutral.log"
    if route == "installer":
        ns = _sandbox(tmp_path, name=f"repo-{arch}")
        # Presence is enough: the request happens before the hash comparison,
        # and the zero digest refuses the install afterwards.
        _checksum_file(ns, tarball, "0" * 64)
        result = _run(
            ns.repo / "tools" / "beads" / "install.sh",
            home=ns.home,
            path=_path(_path_bin(tmp_path)),
            env_extra={"UNAME_S": os_name, "UNAME_M": arch, "CURL_LOG": str(curl_log), "CURL_SERVE": str(archive)},
        )
        assert result.returncode != 0, "the zero checksum fixture should have refused the install"
    else:
        home = tmp_path / "cloud-home"
        home.mkdir()
        copy = _cloud_copy(tmp_path, root=tmp_path / "cloud-root")
        result = _run(
            copy,
            home=home,
            path=_path(_path_bin(tmp_path)),
            env_extra={"CURL_LOG": str(curl_log), "CURL_SERVE": str(archive), "NEUTRAL_LOG": str(neutral_log)},
        )
        assert result.returncode == 0, "cloud's overall exit-0 convention changed"
    assert _log_lines(curl_log) == [expected], f"the route requested {_log_lines(curl_log)}, not {expected}"


@pytest.mark.parametrize(("route", "os_name", "arch"), ROUTES)
def test_install_routes_install_verified_archive(tmp_path: Path, route: str, os_name: str, arch: str) -> None:
    """Criterion 3, success side: when the downloaded archive's actual hash
    matches the committed checksum, the route installs the versioned binary —
    and never touches the unversioned bd beside it."""
    pin = _pin()
    tarball = f"beads_{pin}_{os_name.lower()}_{arch}.tar.gz"
    archive, digest = _bd_tarball(tmp_path, name=f"verified-{route}-{arch}", version=pin)
    curl_log = tmp_path / "curl.log"
    neutral_log = tmp_path / "neutral.log"
    env = {"CURL_LOG": str(curl_log), "CURL_SERVE": str(archive), "NEUTRAL_LOG": str(neutral_log)}
    if route == "installer":
        ns = _sandbox(tmp_path, name=f"repo-{arch}")
        home = ns.home
        sentinel = _sentinel(home)
        _checksum_file(ns, tarball, digest)
        result = _run(
            ns.repo / "tools" / "beads" / "install.sh",
            home=home,
            path=_path(_path_bin(tmp_path)),
            env_extra={"UNAME_S": os_name, "UNAME_M": arch, **env},
        )
    else:
        home = tmp_path / "cloud-home"
        home.mkdir()
        sentinel = _sentinel(home)
        copy = _cloud_copy(tmp_path, root=tmp_path / "cloud-root", digest=digest)
        result = _run(copy, home=home, path=_path(_path_bin(tmp_path)), env_extra=env)
    assert result.returncode == 0, result.stderr
    assert "mismatch" not in result.stderr.lower(), result.stderr
    assert len(_extractions(home)) == 1, "the verified archive was not extracted exactly once"
    _assert_installed(home, pin, sentinel)


@pytest.mark.parametrize(
    ("route", "fault"),
    [("installer", "wrong-digest"), ("installer", "missing-checksum"), ("cloud", "wrong-digest")],
)
def test_install_routes_refuse_unverified_archive(tmp_path: Path, route: str, fault: str) -> None:
    """Criterion 3, refusal side: an archive whose expected checksum is wrong,
    or a platform with no committed checksum at all, must not reach extraction
    or installation. Cloud's overall exit-0 convention stays as it is."""
    pin = _pin()
    tarball = f"beads_{pin}_linux_amd64.tar.gz"
    expected = f"https://github.com/gastownhall/beads/releases/download/v{pin}/{tarball}"
    archive, _ = _bd_tarball(tmp_path, name=f"refused-{route}-{fault}", version=pin)
    curl_log = tmp_path / "curl.log"
    neutral_log = tmp_path / "neutral.log"
    serve = {"CURL_LOG": str(curl_log), "CURL_SERVE": str(archive), "NEUTRAL_LOG": str(neutral_log)}
    if route == "installer":
        ns = _sandbox(tmp_path, name=f"repo-{fault}")
        home = ns.home
        sentinel = _sentinel(home)
        if fault == "wrong-digest":
            _checksum_file(ns, tarball, "f" * 64)
        result = _run(
            ns.repo / "tools" / "beads" / "install.sh",
            home=home,
            path=_path(_path_bin(tmp_path)),
            env_extra={"UNAME_S": "Linux", "UNAME_M": "amd64", **serve},
        )
        assert result.returncode != 0, "an unverified archive was installed"
        if fault == "wrong-digest":
            assert _log_lines(curl_log) == [expected], f"the download went to {_log_lines(curl_log)}"
            assert "MISMATCH" in result.stderr, result.stderr
        else:
            assert _log_lines(curl_log) == [], "the installer downloaded although no committed checksum exists"
            assert "fail closed" in result.stderr, result.stderr
    else:
        home = tmp_path / "cloud-home"
        home.mkdir()
        sentinel = _sentinel(home)
        copy = _cloud_copy(tmp_path, root=tmp_path / "cloud-root", digest="f" * 64)
        result = _run(copy, home=home, path=_path(_path_bin(tmp_path)), env_extra=serve)
        assert result.returncode == 0, "cloud's overall exit-0 convention changed"
        assert "checksum mismatch" in result.stderr, result.stderr
    assert _extractions(home) == [], "an unverified archive reached extraction"
    assert not (home / ".local" / "bin" / f"bd-{pin}").exists(), "an unverified archive produced an installed binary"
    assert sentinel.read_text(encoding="utf-8").startswith("sentinel:"), "the unversioned bd path was overwritten"


@pytest.mark.parametrize("route", ["installer", "cloud"])
@pytest.mark.parametrize("present", ["exact-pin", "longer-patch", "longer-major", "release-candidate"])
def test_install_routes_skip_only_an_exact_pinned_binary(tmp_path: Path, route: str, present: str) -> None:
    """Criterion 3, already-installed side (loop row L2-4): a route skips the
    download only when the binary already at the versioned destination reports
    exactly `bd version <pin>` on its first line. A binary whose version output
    merely contains the pin (1.3.40, 11.3.4, a release candidate) is not the
    pinned release: the route downloads, verifies and installs over it. The
    spec's Boundary names what the skip still trusts."""
    pin = _pin()
    reported = {
        "exact-pin": pin,
        "longer-patch": f"{pin}0",
        "longer-major": f"1{pin}",
        "release-candidate": f"{pin}-rc.1",
    }[present]
    tarball = f"beads_{pin}_linux_amd64.tar.gz"
    expected = f"https://github.com/gastownhall/beads/releases/download/v{pin}/{tarball}"
    archive, digest = _bd_tarball(tmp_path, name=f"present-{route}-{present}", version=pin)
    curl_log = tmp_path / "curl.log"
    neutral_log = tmp_path / "neutral.log"
    env = {"CURL_LOG": str(curl_log), "CURL_SERVE": str(archive), "NEUTRAL_LOG": str(neutral_log)}
    if route == "installer":
        ns = _sandbox(tmp_path, name=f"repo-{present}")
        home = ns.home
        _checksum_file(ns, tarball, digest)
        script = ns.repo / "tools" / "beads" / "install.sh"
        env.update({"UNAME_S": "Linux", "UNAME_M": "amd64"})
    else:
        home = tmp_path / "cloud-home"
        home.mkdir()
        script = _cloud_copy(tmp_path, root=tmp_path / "cloud-root", digest=digest)
    sentinel = _sentinel(home)
    dest = home / ".local" / "bin" / f"bd-{pin}"
    present_log = tmp_path / "present-bd.log"
    _fake_bd(dest, version=reported, log=present_log)
    before = dest.read_bytes()
    result = _run(script, home=home, path=_path(_path_bin(tmp_path)), env_extra=env)
    assert result.returncode == 0, result.stderr
    if present == "exact-pin":
        assert _log_lines(curl_log) == [], "the route downloaded although the exact pinned binary is installed"
        assert _extractions(home) == [], "the route extracted although the exact pinned binary is installed"
        assert dest.read_bytes() == before, "the route replaced the exact pinned binary"
    else:
        assert _log_lines(curl_log) == [expected], (
            f"a binary reporting {reported!r} was taken as the pinned {pin}: the route did not download"
        )
        assert len(_extractions(home)) == 1, "the verified archive was not extracted exactly once"
        assert dest.read_bytes() != before, f"the binary reporting {reported!r} was left in place"
        _assert_installed(home, pin, sentinel)


def test_cloud_pin_and_checksum_match_repository() -> None:
    """Criterion 4: the standalone cloud setup carries the repository's pin and
    the very digest its referenced checksum file commits — so the two
    installation routes cannot drift apart while both look maintained."""
    pin = _pin()
    text = SETUP.read_text(encoding="utf-8")
    version = re.search(r"^BD_VERSION=(\S+)", text, re.M)
    assert version is not None, "the cloud setup declares no BD_VERSION"
    assert version.group(1) == pin, f"the cloud setup installs bd {version.group(1)}, the repository pins {pin}"
    line = re.search(r"^BD_SHA256=([0-9a-f]{64})(.*)$", text, re.M)
    assert line is not None, "the cloud setup declares no 64-hex-digit BD_SHA256"
    referenced = re.search(r"tools/beads/checksums/(\S+\.sha256)", line.group(2))
    assert referenced is not None, "the BD_SHA256 line names no repository checksum file it should equal"
    name = f"beads_{pin}_linux_amd64.tar.gz.sha256"
    assert referenced.group(1) == name, f"the cloud checksum comment names {referenced.group(1)}, not the pinned {name}"
    sums = REPO_ROOT / "tools" / "beads" / "checksums" / name
    assert sums.is_file(), (
        f"{sums.relative_to(REPO_ROOT)} is missing — commit the verified v{pin} release digest first (bd-1-3-4)"
    )
    parts = sums.read_text(encoding="utf-8").split()
    assert parts, f"{name} is empty"
    assert line.group(1) == parts[0], f"the cloud setup's digest diverges from the committed {name}"


@pytest.mark.parametrize("platform", ["darwin_arm64", "linux_amd64"])
def test_committed_checksums_cover_both_platforms(platform: str) -> None:
    """Criterion 3, committed side (loop row L1-2): the repository installer
    reads one checksum file per supported platform, so each pinned file must
    exist and hold exactly one 64-hex SHA-256 digest. Whether that digest is
    the release's own is established by the recorded release verification
    (plan.md, "Release verification"), not by a synthetic test."""
    pin = _pin()
    sums = REPO_ROOT / "tools" / "beads" / "checksums" / f"beads_{pin}_{platform}.tar.gz.sha256"
    assert sums.is_file(), f"{sums.relative_to(REPO_ROOT)} is missing — the {platform} install would fail closed"
    lines = sums.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1, f"{sums.name} holds {len(lines)} lines, not one digest"
    assert re.fullmatch(r"[0-9a-f]{64}", lines[0].split()[0] if lines[0].split() else ""), (
        f"{sums.name} holds no 64-hex SHA-256 digest: {lines[0]!r}"
    )
