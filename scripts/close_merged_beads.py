#!/usr/bin/env python3
"""close_merged_beads.py — closes beads whose completion a merged commit declared.

A commit that finishes a work item carries a ``Closes-Bead: <id>`` trailer
(``prompts/07-commit.md``). This reconciler reads that declaration out of
merged history and closes what it declares, so closure no longer depends on
someone remembering it (bead coding-harness-l1if, decision Q-1). Without
``--write`` it only reports; writing is required, not forgotten.

What counts, exactly:

- Only the trailer. A ``Closes-Bead:`` line is read from the trailing trailer
  paragraph of the raw commit message, using fixed syntax. Git trailer aliases
  and formatting settings cannot change the declarations. A mention in the body, PR
  prose or any other spelling closes nothing; case variants in the trailer
  block are reported as malformed (decisions.md, "Only the trailer counts").
- Only merged history. Every commit reachable from origin's freshly fetched
  main is scanned, whatever the local HEAD says. The fetch uses a private
  ``refs/close-merged/<uuid>`` ref, deleted after pinning its commit, and leaves
  ``origin/main`` unchanged; an unmerged or local-only trailer closes nothing.
- One identifier per trailer. A value that is not exactly one bead identifier
  (a list, prose, an empty value) is reported as malformed and closes nothing.
- One attempt per bead. Duplicate declarations resolve deterministically to
  the newest declaring commit; an already closed bead is never touched again
  (decisions.md, "Idempotent and quiet").

How it runs:

- The checkout is resolved from this script's location, linked worktrees
  included; closures go through the pinned ``tools/bd`` as normal closures —
  argv calls, never ``--force``.
- The tracker state is read through the one access point,
  ``bead_render.render_pfad()``, and the render is validated line by line
  (``check_bead_export.run``) before anything is attempted. A write run
  refuses a preset ``BEAD_RENDER``: state must come from this machine, not
  from a snapshot that may be stale.
- Preflight failures (fetch, history, render) exit nonzero before any closure.
  Unknown identifiers and malformed declarations are reported, never created
  or guessed; a refused closure is reported and the independent candidates
  still close.
- Every eligible write run ends with ``tools/bd dolt push``, even when nothing
  was left to close — a rerun after a failed publication must still publish.
  What closed locally and what reached the remote tracker are reported
  separately.

Exit codes: 0 = nothing unresolved (or, without ``--write``, a clean report);
1 = preflight failure, unknown or newly reported malformed declarations, refused closures, or
a failed publication. After a published write run, malformed declarations are
remembered locally in the checkout's Git directory: they remain visible but do
not fail subsequent runs. Reporting reads these receipts without writing them.
No history cursor, committed export, PR API or git push.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

REPO_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_SCRIPTS))

import bead_render  # noqa: E402 — the ONE access point to the tracker render (bead 1jg.3)
from check_bead_export import run as check_render_lines  # noqa: E402 — the same line check

TRAILER_KEY = "Closes-Bead"
BEAD_ID = re.compile(rb"[A-Za-z0-9][A-Za-z0-9._-]*")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
# The PR number is read only where the commit message itself states it: a
# GitHub merge-commit subject, or a squash subject's trailing "(#N)". Any other
# number in a message stays a number, never a PR reference.
MERGE_PULL_REQUEST = re.compile(r"^Merge pull request #(\d+)\b")
SQUASH_NUMBER = re.compile(r"\(#(\d+)\)$")

# Read each commit separately, with NUL-framed subject and raw message.
# Unlike control bytes such as 0x1e, NUL cannot occur in a commit message.
COMMIT_FORMAT = "%s%x00%B%x00"
TRAILER_LINE = re.compile(rb"[A-Za-z0-9-]+[ \t]*:")

GIT_TIMEOUT = 30.0
FETCH_TIMEOUT = 60.0
# Overridable so budget tests scale the bound through the environment instead
# of patching a copy of this source.
BD_TIMEOUT = float(os.environ.get("CLOSE_MERGED_BD_TIMEOUT", "60.0"))


class PreflightError(RuntimeError):
    """A precondition failed — nothing may be attempted."""


def _neutral_git_env() -> dict[str, str]:
    """Environment for every Git call: no user or system configuration applies.

    A setting such as ``trailer.separators`` changes how Git formats parsed
    trailers, so a configured machine would silently lose declarations.
    """
    # Runtime configuration (COUNT/KEY_n/VALUE_n and PARAMETERS) overrides
    # config files too. Drop the entire namespace before setting our own paths.
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_CONFIG_")}
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_SYSTEM"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


def _git_bytes(repo: Path, *args: str, timeout: float = GIT_TIMEOUT) -> bytes:
    try:
        erg = subprocess.run(
            ["git", "-c", "trailer.separators=:", *args],
            cwd=repo,
            capture_output=True,
            timeout=timeout,
            env=_neutral_git_env(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PreflightError(f"git {args[0]} failed: {exc}") from None
    if erg.returncode != 0:
        diagnostic = (erg.stderr or erg.stdout).decode("utf-8", errors="replace").strip()
        raise PreflightError(f"git {args[0]} failed: {diagnostic}")
    return erg.stdout


def _git(repo: Path, *args: str, timeout: float = GIT_TIMEOUT) -> str:
    return _git_bytes(repo, *args, timeout=timeout).decode("utf-8", errors="replace")


def resolve_checkout() -> tuple[Path, Path]:
    """Reconcile the checkout containing this script, including linked worktrees."""
    try:
        top = _git(REPO_SCRIPTS, "rev-parse", "--show-toplevel").strip()
    except PreflightError as exc:
        raise PreflightError(f"not inside a git checkout ({exc})") from None
    root = Path(top)
    bd = root / "tools" / "bd"
    if not (bd.is_file() and os.access(bd, os.X_OK)):
        raise PreflightError(f"the pinned wrapper is missing or not executable: {bd}")
    return root, bd


def fetch_and_pin(root: Path) -> str:
    """Fetch origin's main and pin the commit this run reads — never a stale ref."""
    # Each run owns its ref; background status-line fetches own FETCH_HEAD.
    ref = f"refs/close-merged/{uuid.uuid4().hex}"
    try:
        _git(
            root,
            "fetch",
            "--no-write-fetch-head",
            "--refmap=",
            "origin",
            f"+refs/heads/main:{ref}",
            timeout=FETCH_TIMEOUT,
        )
        pinned = _git(root, "rev-parse", f"{ref}^{{commit}}").strip()
    finally:
        _git(root, "update-ref", "-d", ref)
    if not FULL_SHA.match(pinned):
        raise PreflightError(f"origin's main does not resolve to a commit sha ({pinned!r})")
    if _git(root, "rev-parse", "--is-shallow-repository").strip() == "true":
        raise PreflightError("this checkout is shallow — merged history cannot be read completely")
    return pinned


def load_state() -> dict[str, dict]:
    """Tracker state through the one access point, validated before any use."""
    try:
        render = bead_render.render_pfad()
    except (OSError, bead_render.RendererNichtMoeglich, SystemExit) as exc:
        raise PreflightError(f"the tracker render is not readable: {exc}") from None
    findings = check_render_lines(render)
    if findings:
        raise PreflightError("the tracker render is not valid: " + "; ".join(findings))
    state: dict[str, dict] = {}
    for line in render.read_text(encoding="utf-8").splitlines():
        if line.strip():
            satz = json.loads(line)
            state[satz["id"]] = satz
    return state


def collect_declarations(root: Path, pinned: str) -> tuple[dict[str, tuple[str, str]], list[tuple[str, str]]]:
    """Valid and malformed declarations, from a newest-first traversal of ALL
    commits reachable from the pinned sha — not first-parent, not HEAD.

    The first declaring commit in this order wins, so a duplicate declaration
    resolves deterministically to the newest one. Returns (declarations,
    malformed): bead id -> (declaring sha, subject), and the malformed values
    with their commits.
    """
    out = _git_bytes(root, "log", "-z", "--format=%H", pinned)
    declarations: dict[str, tuple[str, str]] = {}
    malformed: list[tuple[str, str]] = []
    key = TRAILER_KEY.encode("ascii")
    for raw_sha in out.split(b"\x00"):
        if not raw_sha:
            continue
        sha = raw_sha.decode("ascii")
        if not FULL_SHA.fullmatch(sha):
            raise PreflightError("merged history returned an invalid commit SHA")
        record = _git_bytes(root, "log", "-1", f"--format={COMMIT_FORMAT}", sha)
        fields = record.split(b"\x00")
        if len(fields) != 3 or fields[2] != b"\n":
            raise PreflightError(f"cannot read complete trailer fields for {sha}")
        subject = fields[0].decode("utf-8", errors="replace")
        for line in raw_trailers(fields[1]):
            raw_key, _, raw_value = line.partition(b":")
            raw_key = raw_key.rstrip(b" \t")
            if raw_key.lower() != key.lower():
                continue
            # Horizontal padding is syntax; embedded CR and other control
            # bytes remain value data after line-ending normalization.
            raw_value = raw_value.strip(b" \t")
            value = raw_value.decode("utf-8", errors="replace")
            if raw_key != key:
                malformed.append((sha, line.decode("utf-8", errors="replace")))
            elif BEAD_ID.fullmatch(raw_value):
                declarations.setdefault(value, (sha, subject))
            else:
                malformed.append((sha, value))
    return declarations, malformed


def raw_trailers(message: bytes) -> list[bytes]:
    """Read the final trailer paragraph without consulting Git configuration.

    Normalize CRLF to LF, leaving embedded CR and other control bytes inside
    values. Git's patch boundary ends the message before trailer selection.
    A trailer block follows a blank line after the subject and contains trailer
    lines and their indented continuations, never body prose.
    Fold continuations before validating values so a first-line identifier
    cannot become a declaration on its own.
    """
    lines = message.replace(b"\r\n", b"\n").split(b"\n")
    for index, line in enumerate(lines):
        if line == b"---":
            lines = lines[:index]
            break
    while lines and not lines[-1].strip(b" \t"):
        lines.pop()
    start = len(lines)
    while start and lines[start - 1].strip(b" \t"):
        start -= 1
    if start < 2:
        return []  # The subject itself is never a completion declaration.
    trailers: list[bytes] = []
    for line in lines[start:]:
        if line.startswith((b" ", b"\t")) and trailers:
            trailers[-1] += b" " + line.lstrip(b" \t")
        elif TRAILER_LINE.match(line):
            trailers.append(line)
        else:
            return []
    return trailers


def explicit_pr(subject: str) -> str | None:
    """The PR number, only where the commit message itself states it."""
    merge = MERGE_PULL_REQUEST.match(subject)
    if merge:
        return merge.group(1)
    squash = SQUASH_NUMBER.search(subject)
    if squash:
        return squash.group(1)
    return None


def closure_reason(sha: str, subject: str) -> str:
    """The closure reason: the declaring commit, and the PR where it says one."""
    reason = f"merged into main: declared by commit {sha}"
    pr = explicit_pr(subject)
    return f"{reason} (PR #{pr})" if pr else reason


def _unresolved(unknown: list[str], malformed: list[tuple[str, str]]) -> None:
    """Reports declarations that resolve to nothing — never created, never guessed."""
    for bid in unknown:
        print(f"unknown bead (not created): {bid}", file=sys.stderr)
    for sha, value in malformed:
        print(f"malformed {TRAILER_KEY} value in {sha}: {value!r}", file=sys.stderr)


def malformed_receipts(root: Path) -> tuple[Path, set[tuple[str, str]]]:
    """Local acknowledgements, not a history cursor: every run still scans all commits."""
    path = Path(_git(root, "rev-parse", "--git-path", "close-merged-malformed.json").strip())
    if not path.is_absolute():
        path = root / path
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list) or any(
            not isinstance(row, list)
            or len(row) != 2
            or not all(isinstance(value, str) for value in row)
            or not FULL_SHA.fullmatch(row[0])
            for row in data
        ):
            raise ValueError("expected pairs of commit SHA and malformed value")
        return path, {tuple(row) for row in data}
    except FileNotFoundError:
        return path, set()
    except (OSError, ValueError) as exc:
        raise PreflightError(f"malformed declaration receipts are unreadable: {exc}") from None


def save_malformed_receipts(path: Path, receipts: set[tuple[str, str]]) -> None:
    """Replace atomically so interruption cannot leave a partial receipt file."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(sorted(receipts), stream)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Close beads whose completion a merged Closes-Bead trailer declared.",
        epilog=(
            "Exit status: 0 = nothing unresolved; 1 = preflight failure or unresolved work "
            "(unknown/new malformed declarations, refused closures, failed publication). "
            "Read-only reporting also fails on unresolved declarations; previously reported malformed "
            "trailers remain visible but do not fail again after a published write run."
        ),
    )
    ap.add_argument("--write", action="store_true", help="close eligible beads and publish; without it, only report")
    ap.add_argument("--budget-seconds", type=float, help="startup budget shared by closures and publication")
    args = ap.parse_args(argv)
    if args.budget_seconds is not None and args.budget_seconds <= 0:
        ap.error("--budget-seconds must be positive")
    deadline = time.monotonic() + args.budget_seconds if args.budget_seconds is not None else None

    if args.write and os.environ.get(bead_render.UMGEBUNGS_RENDER, "").strip():
        print(
            f"close-merged: refusing to write with {bead_render.UMGEBUNGS_RENDER} set — the state would be a "
            "preset render, not this machine's tracker; unset it for a write run.",
            file=sys.stderr,
        )
        return 1

    try:
        root, bd = resolve_checkout()
        pinned = fetch_and_pin(root)
        state = load_state()
        declarations, malformed = collect_declarations(root, pinned)
        receipt_path, receipts = malformed_receipts(root) if malformed else (None, set())
        new_malformed = set(malformed) - receipts
    except PreflightError as exc:
        print(f"close-merged: preflight failed, nothing attempted: {exc}", file=sys.stderr)
        return 1

    unknown = [bid for bid in declarations if bid not in state]
    eligible = [
        (bid, sha, subject)
        for bid, (sha, subject) in declarations.items()
        if bid in state and state[bid]["status"] != "closed"
    ]

    if not args.write:
        print(
            f"close-merged: report over {pinned[:12]} — {len(eligible)} eligible, "
            f"{len(unknown)} unknown, {len(malformed)} malformed"
        )
        for bid, sha, subject in eligible:
            print(f"would close {bid} ({closure_reason(sha, subject)})")
        _unresolved(unknown, malformed)
        return 1 if (unknown or new_malformed) else 0

    closed: list[str] = []
    refused: list[tuple[str, str]] = []
    for bid, sha, subject in eligible:
        reason = closure_reason(sha, subject)
        # Bound each close by the remaining budget, but refuse to start with
        # less than one second: process startup/timeout cleanup can overshoot
        # a tiny timeout. Publication is still attempted after the batch.
        close_timeout = BD_TIMEOUT if deadline is None else min(BD_TIMEOUT, deadline - time.monotonic())
        if close_timeout < 1.0:
            refused.append((bid, "startup budget exhausted"))
            print(f"refused: {bid}: startup budget exhausted; retry reconciliation", file=sys.stderr)
            continue
        try:
            erg = subprocess.run(
                [str(bd), "close", bid, f"--reason={reason}"],
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=close_timeout,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            refused.append((bid, str(exc)))
            print(f"refused: {bid}: {exc}", file=sys.stderr)
            continue
        if erg.returncode == 0:
            closed.append(bid)
            print(f"closed {bid} ({reason})")
        else:
            detail = (erg.stderr or erg.stdout).strip()
            refused.append((bid, detail))
            print(f"refused: {bid}: {detail}", file=sys.stderr)

    try:
        push_timeout = BD_TIMEOUT if deadline is None else max(0.01, min(BD_TIMEOUT, deadline - time.monotonic()))
        push = subprocess.run(
            [str(bd), "dolt", "push"],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=push_timeout,
        )
        published = push.returncode == 0
        if not published:
            print(f"close-merged: publication failed: {(push.stderr or push.stdout).strip()}", file=sys.stderr)
    except (OSError, subprocess.TimeoutExpired) as exc:
        published = False
        print(f"close-merged: publication failed: {exc}", file=sys.stderr)

    _unresolved(unknown, malformed)
    print(f"local closures: {len(closed)} ({len(refused)} refused) · published: {'yes' if published else 'NO'}")
    if published and new_malformed:
        try:
            save_malformed_receipts(receipt_path, receipts | new_malformed)
        except OSError as exc:
            print(f"close-merged: could not record malformed declaration receipts: {exc}", file=sys.stderr)
            return 1
    return 1 if (unknown or new_malformed or refused or not published) else 0


if __name__ == "__main__":
    # Diagnostics and summaries use UTF-8 too, independently of the locale.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
