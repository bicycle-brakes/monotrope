"""Bounded local Git history and the shared local-only Git transport.

History collection performs no model operation, tracker read, working-file
read, network fetch or retry. The snapshot helper also uses the local Git
transport for its inventory. All commands share the caller's run deadline.
"""

from __future__ import annotations

import math
import os
import re
import subprocess
import time
from datetime import UTC, datetime
from pathlib import PurePosixPath


class ResearchHistoryError(ValueError):
    """History preparation failed; the caller must stop before topics (exit 1)."""

    exit_code = 1


def _git(root, deadline, *args):
    seconds = deadline - time.monotonic()
    if seconds <= 0:
        raise ResearchHistoryError("history deadline expired")
    env = {key: value for key, value in os.environ.items() if key in {"PATH", "LANG", "LC_ALL", "LC_CTYPE"}}
    env.update(
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_CONFIG_SYSTEM=os.devnull,
        GIT_CONFIG_NOSYSTEM="1",
        GIT_NO_LAZY_FETCH="1",
        GIT_ALLOW_PROTOCOL="",
        GIT_TERMINAL_PROMPT="0",
        GIT_NO_REPLACE_OBJECTS="1",
        GIT_LITERAL_PATHSPECS="1",
        GIT_OPTIONAL_LOCKS="0",
    )
    try:
        result = subprocess.run(
            [
                "git",
                "--no-pager",
                "-C",
                str(root),
                "-c",
                "core.fsmonitor=false",
                "-c",
                "core.hooksPath=" + os.devnull,
                *args,
            ],
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=seconds,
            check=False,
        )
    except (OSError, ValueError, UnicodeError, subprocess.TimeoutExpired) as error:
        raise ResearchHistoryError(f"local history command failed: {type(error).__name__}") from error
    if result.returncode:
        raise ResearchHistoryError("local history command failed: " + result.stderr.strip()[:500])
    return result.stdout


def _without_formatter_newline(text):
    return text[:-1] if text.endswith("\n") else text


def build_research_history(root, frozen_head, mapped_paths, *, deadline):
    """Retain up to ten commit records per mapped path, deduplicated by full hash.

    The eleventh hash only measures whether older history remains unread; no
    eleventh commit body is read. Global/lazy-fetch/replacement configuration
    cannot change this frozen local evidence. The body cap counts Unicode.
    """
    if type(deadline) not in (int, float) or not math.isfinite(deadline):
        raise ResearchHistoryError("history deadline must be a finite monotonic timestamp")
    if not isinstance(frozen_head, str) or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", frozen_head):
        raise ResearchHistoryError("history needs a full frozen commit hash")
    if not isinstance(mapped_paths, list):
        raise ResearchHistoryError("mapped history paths must be a list")
    paths = []
    for path in mapped_paths:
        if not isinstance(path, str) or not path or "\0" in path or "\\" in path:
            raise ResearchHistoryError("invalid mapped history path")
        parsed = PurePosixPath(path)
        if parsed.is_absolute() or not parsed.parts or ".." in parsed.parts or str(parsed) != path:
            raise ResearchHistoryError("invalid mapped history path")
        if path not in paths:
            paths.append(path)
    paths.sort()
    if _git(root, deadline, "cat-file", "-t", frozen_head).strip() != "commit":
        raise ResearchHistoryError("frozen history object is not a commit")
    shallow = _git(root, deadline, "rev-parse", "--is-shallow-repository").strip()
    if shallow not in ("true", "false"):
        raise ResearchHistoryError("cannot measure local history completeness")
    by_path, not_read = {}, []
    for path in paths:
        hashes = _git(
            root, deadline, "log", "--no-show-signature", "--format=%H", "--max-count=11", frozen_head, "--", path
        ).splitlines()
        if len(hashes) > 11 or any(not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", item) for item in hashes):
            raise ResearchHistoryError("malformed history identity")
        by_path[path] = hashes[:10]
        if len(hashes) > 10 or shallow == "true":
            not_read.append(
                {
                    "path": path,
                    "reason": "older history outside the ten-commit local packet",
                    "shallow": shallow == "true",
                }
            )
        elif not hashes:
            not_read.append(
                {"path": path, "reason": "no committed history at frozen HEAD", "outcome": "measured-empty"}
            )
    commits = {}
    selected = sorted({item for hashes in by_path.values() for item in hashes})
    for sha in selected:
        metadata = _without_formatter_newline(
            _git(root, deadline, "show", "-s", "--no-show-signature", "--format=%H%x00%aI%x00%s", sha)
        ).split("\0", 2)
        if len(metadata) != 3 or metadata[0] != sha:
            raise ResearchHistoryError("malformed history metadata")
        try:
            authored = datetime.fromisoformat(metadata[1])
            if authored.tzinfo is None:
                raise ValueError("missing timezone")
            authored_utc = authored.astimezone(UTC).isoformat().replace("+00:00", "Z")
        except ValueError as error:
            raise ResearchHistoryError("malformed history author date") from error
        body = _without_formatter_newline(_git(root, deadline, "show", "-s", "--no-show-signature", "--format=%b", sha))
        touched = _git(
            root,
            deadline,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "--no-ext-diff",
            "--no-textconv",
            "-m",
            "-r",
            "--root",
            "-z",
            sha,
        ).split("\0")
        commits[sha] = {
            "hash": sha,
            "author_utc": authored_utc,
            "subject": metadata[2],
            "body": body[:4000],
            "body_truncated": len(body) > 4000,
            "touched_mapped_paths": sorted(set(touched) & set(paths)),
        }
    return {"frozen_head": frozen_head, "paths": by_path, "commits": commits, "not_read": not_read}
