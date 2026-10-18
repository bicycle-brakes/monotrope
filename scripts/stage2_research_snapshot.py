"""Transient frozen research inputs; model dispatch belongs to the runner."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import stat
import tempfile
import time
from pathlib import Path, PurePosixPath

from stage2_research_history import ResearchHistoryError, _git


class ResearchSnapshotError(ValueError):
    """Preparation or drift-check failure, never successful empty evidence."""

    exit_code = 1


def _relative(path):
    if not isinstance(path, str) or not path or "\0" in path or "\\" in path:
        raise ResearchSnapshotError("invalid frozen input path")
    parsed = PurePosixPath(path)
    if not parsed.parts or parsed.is_absolute() or ".." in parsed.parts or str(parsed) != path:
        raise ResearchSnapshotError("invalid frozen input path")
    return parsed


def _remaining(deadline):
    if time.monotonic() >= deadline:
        raise ResearchSnapshotError("frozen input deadline expired")


def _read(root, path, deadline):
    """Never follow a file or directory symlink to an ambient input."""
    parts = _relative(path).parts
    _remaining(deadline)
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            _remaining(deadline)
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        child = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        os.close(fd)
        fd = child
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ResearchSnapshotError("frozen input is not a regular file: " + path)
        chunks = []
        while True:
            _remaining(deadline)
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)
    except OSError as error:
        raise ResearchSnapshotError("cannot freeze input: " + path) from error
    finally:
        os.close(fd)


def _inventory(root, change, deadline):
    tracked = _git(root, deadline, "ls-files", "--cached", "-z").split("\0")
    untracked = _git(root, deadline, "ls-files", "--others", "--exclude-standard", "-z", "--", change).split("\0")
    result = []
    for values in (tracked, untracked):
        paths = [value for value in values if value]
        if len(set(paths)) != len(paths):
            raise ResearchSnapshotError("ambiguous frozen input inventory")
        for path in paths:
            _relative(path)
        result.append(set(paths))
    return result


def _without_updated(data):
    match = re.match(rb"---\r?\n(.*?)\r?\n---", data, re.S)
    if not match:
        return data
    header = re.sub(rb"(?m)^updated:[^\r\n]*", b"updated:", match.group(1), count=1)
    return data[: match.start(1)] + header + data[match.end(1) :]


class FrozenResearchState:
    """Own the disposable copies until publication or abort, then delete them."""

    def __init__(self, root, change, deadline, scratch):
        self.root = root
        self.change = change
        self.deadline = deadline
        self._scratch = scratch
        self.directory = Path(scratch.name)
        self._files = {}

    def __enter__(self):
        return self

    def __exit__(self, *_exception):
        self.close()

    def close(self):
        self._scratch.cleanup()

    def sources(self):
        return {path: copy.read_bytes() for path, copy in self._files.items()}

    def manifest(self):
        return json.loads(json.dumps(self._manifest))

    def changed_paths(self, *, owned_research_bytes=None):
        """Only the exact caller-owned research append/restamp may be exempt."""
        try:
            tracked, untracked = _inventory(self.root, self.change, self.deadline)
            changed = self._tracked ^ tracked | self._untracked ^ untracked
            if _git(self.root, self.deadline, "rev-parse", "--verify", "HEAD").strip() != self._manifest["head"]:
                changed.add("HEAD")
            research = self.change + "/research.md"
            if owned_research_bytes is not None:
                if not isinstance(owned_research_bytes, bytes) or research not in self._files:
                    raise ResearchSnapshotError("invalid runner-owned research bytes")
                if not _without_updated(owned_research_bytes).startswith(
                    _without_updated(self._files[research].read_bytes())
                ):
                    raise ResearchSnapshotError("runner-owned research must preserve its frozen prefix")
            for path, copy in self._files.items():
                try:
                    now = _read(self.root, path, self.deadline)
                except ResearchSnapshotError:
                    changed.add(path)
                    continue
                expected = (
                    owned_research_bytes if path == research and owned_research_bytes is not None else copy.read_bytes()
                )
                if now != expected:
                    changed.add(path)
            return sorted(changed)
        except (OSError, ResearchHistoryError) as error:
            raise ResearchSnapshotError("cannot check frozen input state") from error


def freeze_research_state(root, change, *, deadline, scratch_parent=None):
    """Freeze working bytes, including untracked non-ignored change inputs."""
    _relative(change)
    if type(deadline) not in (int, float) or not math.isfinite(deadline):
        raise ResearchSnapshotError("frozen input deadline must be a finite timestamp")
    root = Path(root).resolve(strict=True)
    scratch = tempfile.TemporaryDirectory(prefix="research-inputs-", dir=scratch_parent)
    state = FrozenResearchState(root, change, deadline, scratch)
    try:
        if state.directory.resolve().is_relative_to(root):
            raise ResearchSnapshotError("frozen copies must stay outside the repository")
        head = _git(root, deadline, "rev-parse", "--verify", "HEAD").strip()
        if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", head):
            raise ResearchSnapshotError("invalid frozen HEAD")
        tracked, untracked = _inventory(root, change, deadline)
        if tracked & untracked:
            raise ResearchSnapshotError("ambiguous tracked/untracked inventory")
        state._tracked, state._untracked = tracked, untracked
        digests = {}
        for index, path in enumerate(sorted(tracked | untracked)):
            data = _read(root, path, deadline)
            copy = state.directory / str(index)
            copy.write_bytes(data)
            state._files[path] = copy
            digests[path] = hashlib.sha256(data).hexdigest()
        digest = hashlib.sha256(
            json.dumps({"head": head, "paths": digests}, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        state._manifest = {
            "head": head,
            "digest": digest,
            "paths": digests,
            "untracked": {path: digests[path] for path in sorted(untracked)},
        }
        if state.changed_paths():
            raise ResearchSnapshotError("inputs changed while being frozen")
        return state
    except BaseException as error:
        state.close()
        if isinstance(error, ResearchSnapshotError):
            raise
        if isinstance(error, OSError | ValueError):
            raise ResearchSnapshotError("cannot freeze research inputs") from error
        raise


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def stored_binding(manifest, research_path, research_bytes, *, append=None):
    """The resume binding of one frozen state, in the shape the state store keeps (Q-13).

    ``research_bytes`` are the frozen bytes of ``research_path``; ``append`` are the exact bytes
    the runner will add to it, recorded before the write so a crash between the two is covered.
    """
    paths = dict(manifest["paths"])
    if research_path not in paths or paths[research_path] != _sha256(research_bytes):
        raise ResearchSnapshotError("research bytes do not belong to the frozen state")
    binding = {
        "paths": paths,
        "research": research_path,
        "research_normalised_sha256": _sha256(_without_updated(research_bytes)),
    }
    if append is not None:
        if not isinstance(append, bytes):
            raise ResearchSnapshotError("invalid runner-owned research bytes")
        binding["append"] = {"sha256": _sha256(append), "length": len(append)}
    return binding


def changed_against_stored(manifest, research_path, research_bytes, stored):
    """Paths whose bytes differ from a stored binding; empty means the binding holds.

    HEAD is not compared. ``research.md`` is compared without the stored run's own appended tail
    (its length and digest must both match) and without the ``updated:`` restamp.
    """
    try:
        research = stored["research"]
        stored_paths = stored["paths"]
        normalised = stored["research_normalised_sha256"]
        append = stored.get("append")
    except (KeyError, TypeError) as error:
        raise ResearchSnapshotError("malformed stored binding") from error
    if research != research_path:
        raise ResearchSnapshotError("stored binding names another research path")
    current = manifest["paths"]
    changed = {
        path
        for path in set(current) | set(stored_paths)
        if path != research and current.get(path) != stored_paths.get(path)
    }
    candidates = [research_bytes]  # the append was recorded but never written, or there was none
    if append is not None and 0 < append["length"] <= len(research_bytes):
        cut = len(research_bytes) - append["length"]
        if _sha256(research_bytes[cut:]) == append["sha256"]:
            candidates.append(research_bytes[:cut])
    present = research in current and research in stored_paths
    if not present or all(_sha256(_without_updated(body)) != normalised for body in candidates):
        changed.add(research)
    return sorted(changed)
