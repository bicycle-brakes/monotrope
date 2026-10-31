#!/usr/bin/env python3
"""close_merged_beads.py — closes beads whose completion a merged commit declared.

A commit that finishes a work item carries a ``Closes-Bead: <id>`` trailer
(``prompts/07-commit.md``). This reconciler reads that declaration out of
merged history and closes what it declares, so closure no longer depends on
someone remembering it (bead coding-harness-l1if, decision Q-1). Without
``--write`` it only reports; writing is required, not forgotten.

What counts, exactly:

- Only the trailer. A ``Closes-Bead:`` line is read where Git reads trailers —
  the trailing trailer block of a commit message. A mention in the body, PR
  prose or any other spelling closes nothing (decisions.md, "Only the trailer
  counts").
- Only merged history. Every commit reachable from a freshly fetched
  ``origin/main`` is scanned, whatever the local HEAD says; a trailer on an
  unmerged or local-only commit closes nothing.
- One identifier per trailer. A value that is not exactly one bead identifier
  (a list, prose, an empty value) is reported as malformed and closes nothing.
- One attempt per bead. Duplicate declarations resolve deterministically to
  the newest declaring commit; an already closed bead is never touched again
  (decisions.md, "Idempotent and quiet").

How it runs:

- The checkout is resolved from the working directory, linked worktrees
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
1 = preflight failure, or unknown/malformed declarations, refused closures, or
a failed publication. No cursor, committed export, PR API or git push.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_SCRIPTS))

import bead_render  # noqa: E402 — the ONE access point to the tracker render (bead 1jg.3)
from check_bead_export import run as check_render_lines  # noqa: E402 — the same line check

TRAILER_KEY = "Closes-Bead"
BEAD_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
# The PR number is read only where the commit message itself states it: a
# GitHub merge-commit subject, or a squash subject's trailing "(#N)". Any other
# number in a message stays a number, never a PR reference.
MERGE_PULL_REQUEST = re.compile(r"^Merge pull request #(\d+)\b")
SQUASH_NUMBER = re.compile(r"\(#(\d+)\)$")

# One record per commit, delimited by 0x1e, fields by NUL: sha, subject, and
# the raw trailer lines Git parsed. This file only reads the exact
# ``Closes-Bead:`` lines out of them — case-sensitive, by design: the key is
# exactly Closes-Bead, and any other spelling is prose.
LOG_FORMAT = "%H%x00%s%x00%(trailers:only=true,unfold=false)%x1e"

GIT_TIMEOUT = 30.0
FETCH_TIMEOUT = 60.0
BD_TIMEOUT = 60.0


class PreflightError(RuntimeError):
    """A precondition failed — nothing may be attempted."""


def _git(repo: Path, *args: str, timeout: float = GIT_TIMEOUT) -> str:
    try:
        erg = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PreflightError(f"git {args[0]} failed: {exc}") from None
    if erg.returncode != 0:
        raise PreflightError(f"git {args[0]} failed: {(erg.stderr or erg.stdout).strip()}")
    return erg.stdout


def resolve_checkout() -> tuple[Path, Path]:
    """The checkout to reconcile, from the working directory — worktrees included."""
    try:
        top = _git(Path.cwd(), "rev-parse", "--show-toplevel").strip()
    except PreflightError as exc:
        raise PreflightError(f"not inside a git checkout ({exc})") from None
    root = Path(top)
    bd = root / "tools" / "bd"
    if not (bd.is_file() and os.access(bd, os.X_OK)):
        raise PreflightError(f"the pinned wrapper is missing or not executable: {bd}")
    return root, bd


def fetch_and_pin(root: Path) -> str:
    """Fetch origin's main and pin the commit this run reads — never a stale ref."""
    _git(root, "fetch", "origin", "main", timeout=FETCH_TIMEOUT)
    try:
        pinned = _git(root, "rev-parse", "FETCH_HEAD^{commit}").strip()
    except PreflightError as exc:
        raise PreflightError(f"origin's main is not readable as a commit ({exc})") from None
    if not FULL_SHA.match(pinned):
        raise PreflightError(f"origin's main does not resolve to a commit sha ({pinned!r})")
    if _git(root, "rev-parse", "--is-shallow-repository").strip() == "true":
        raise PreflightError("this checkout is shallow — merged history cannot be read completely")
    return pinned


def load_state() -> dict[str, dict]:
    """Tracker state through the one access point, validated before any use."""
    try:
        render = bead_render.render_pfad()
    except (FileNotFoundError, bead_render.RendererNichtMoeglich) as exc:
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
    out = _git(root, "log", f"--format={LOG_FORMAT}", pinned)
    declarations: dict[str, tuple[str, str]] = {}
    malformed: list[tuple[str, str]] = []
    prefix = f"{TRAILER_KEY}:"
    for record in out.split("\x1e"):
        fields = record.split("\x00")
        if len(fields) < 3:
            continue
        sha, subject, trailer_block = fields[0].strip(), fields[1], fields[2]
        for line in trailer_block.splitlines():
            if not line.startswith(prefix):
                continue
            value = line[len(prefix) :].strip()
            if BEAD_ID.match(value):
                declarations.setdefault(value, (sha, subject))
            else:
                malformed.append((sha, value))
    return declarations, malformed


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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Close beads whose completion a merged Closes-Bead trailer declared.")
    ap.add_argument("--write", action="store_true", help="close eligible beads and publish; without it, only report")
    args = ap.parse_args(argv)

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
    except PreflightError as exc:
        print(f"close-merged: preflight failed, nothing attempted: {exc}", file=sys.stderr)
        return 1

    declarations, malformed = collect_declarations(root, pinned)
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
        return 1 if (unknown or malformed) else 0

    closed: list[str] = []
    refused: list[tuple[str, str]] = []
    for bid, sha, subject in eligible:
        reason = closure_reason(sha, subject)
        try:
            erg = subprocess.run(
                [str(bd), "close", bid, f"--reason={reason}"],
                cwd=root,
                capture_output=True,
                text=True,
                timeout=BD_TIMEOUT,
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
        push = subprocess.run([str(bd), "dolt", "push"], cwd=root, capture_output=True, text=True, timeout=BD_TIMEOUT)
        published = push.returncode == 0
        if not published:
            print(f"close-merged: publication failed: {(push.stderr or push.stdout).strip()}", file=sys.stderr)
    except (OSError, subprocess.TimeoutExpired) as exc:
        published = False
        print(f"close-merged: publication failed: {exc}", file=sys.stderr)

    _unresolved(unknown, malformed)
    print(f"local closures: {len(closed)} ({len(refused)} refused) · published: {'yes' if published else 'NO'}")
    return 1 if (unknown or malformed or refused or not published) else 0


if __name__ == "__main__":
    sys.exit(main())
