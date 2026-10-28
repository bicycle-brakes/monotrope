#!/usr/bin/env python3
"""pr_sync.py — one supported merge that regenerates the plans index, and an
on-request sync for open pull-request branches.

`plans/INDEX.md` is generated, but committed: a merge that kept either
parent's index would age the list exactly like a hand-kept one, and Git
resolves a textually clean index merge into precisely such a lie. This helper
therefore never takes the index from a merge result — it renders
`plans/INDEX.md` from the complete merged plans tree with the committed
renderer, and publishes only that (beads coding-harness-hfsz,
coding-harness-njtm, coding-harness-eq6y).

Two commands share one merge engine:

    python3 scripts/pr_sync.py merge-main --root .
        Merges the fetched `origin/main` into the current branch of `--root`
        and applies the result as a fast-forward. For a hand merge and for
        preparing phase 6. Refuses a detached HEAD, `main` itself, an
        in-progress merge or rebase, and a dirty checkout. Never pushes.

    python3 scripts/pr_sync.py sync --root .
        Discovers every open pull request with `gh`, and updates each eligible
        branch by pushing a merge of `origin/main` with a regenerated index.
        Called explicitly by the day session or the night orchestrator — no
        scheduled job runs it. GitHub's server-side "Update branch" and merge
        buttons cannot run this helper; the unchanged `plans-registry` gate
        stays their backstop.

The sync skips, and reports, what it must not touch: fork pull requests and
bases other than `main` (outside scope); decision pull requests (the
`decision` label or a `decide(` title), branches changing a runner-held or
human-decided path, and branches checked out locally with uncommitted or
unpushed work (protected). A conflict outside the index is reported with its
paths and stops that branch. Protection policy and renderer are read from the
invoking committed tree, never from candidate pull-request code. Pushes carry
an exact expected-head lease, so a racing writer's commit is left intact and
reported as a moved branch. Pull requests older than five working days are
listed for the maintainer, whatever their protection.

Exit codes: 0 for a measured pass (expected protected and outside skips are
not errors), 1 for conflicts and errors, 2 for an invalid invocation or a
refused local merge. A discovery or fetch failure is an error — it can never
yield an empty successful pass.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

import yaml

INDEX_PATH = "plans/INDEX.md"
GIT_SECONDS = 120
RENDER_SECONDS = 300
GH_SECONDS = 120
WORKING_DAYS_OVERDUE = 5

LIST_FIELDS = "number,url,title,createdAt,baseRefName,headRefName,headRefOid,isCrossRepository,labels,files"
VIEW_FIELDS = "state,number,url,title,createdAt,baseRefName,headRefName,headRefOid,isCrossRepository,labels,files"

_TREE_OID = re.compile(r"[0-9a-f]{40}")
# One conflicted-file-info entry: `<mode> <oid> <stage>` and the path. Their
# separator changed across Git versions (blank, tab, NUL or line end), and a
# miss here would read a real conflict as clean — so one pattern reads every
# shape, and a conflict Git reports without a readable entry is refused.
_CONFLICT_ENTRY = re.compile(r"[0-7]{6} [0-9a-f]{40} [1-3](?:[ \t]|\0|\r?\n)([^\0\n\r]+)")


class Failed(Exception):
    """Something could not be measured; the affected branch stays untouched."""


class Refused(Exception):
    """The local state is one this helper never merges in."""


class MetadataError(Exception):
    """One pull request's reported metadata is absent or malformed."""


@dataclass
class Pull:
    """One open pull request as `gh` reports it."""

    number: int
    url: str
    title: str
    created: dt.datetime
    base: str
    branch: str
    head: str
    cross_repository: bool
    labels: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)


@dataclass
class Prepared:
    """A merge commit that is fully built but not yet published."""

    oid: str
    detail: str


# ---------------------------------------------------------------------------
# Git plumbing — argument arrays only, never shell text from ref or PR data.
# ---------------------------------------------------------------------------


def git(
    root: Path, *args: str, timeout: int = GIT_SECONDS, env: dict | None = None, data: bytes | None = None
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args], input=data, capture_output=True, timeout=timeout, check=False, env=env
        )
    except subprocess.TimeoutExpired as error:
        raise Failed(f"git {' '.join(args[:2])} did not finish within {timeout} seconds") from error
    except OSError as error:
        raise Failed(f"git could not be started: {error}") from error


def git_out(root: Path, *args: str, env: dict | None = None) -> str:
    done = git(root, *args, env=env)
    if done.returncode != 0:
        detail = (done.stderr or done.stdout).decode("utf-8", "replace").strip().splitlines()
        raise Failed(f"git {' '.join(args[:2])} failed: {detail[-1] if detail else done.returncode}")
    return done.stdout.decode("utf-8", "replace")


def tail(text: bytes, limit: int = 3) -> str:
    lines = text.decode("utf-8", "replace").strip().splitlines()
    return " | ".join(lines[-limit:]) if lines else "(no output)"


def ensure_repo(root: Path) -> None:
    done = git(root, "rev-parse", "--git-dir")
    if done.returncode != 0:
        raise Refused(f"{root} is not a git worktree")


def fetch_origin(root: Path) -> None:
    done = git(root, "fetch", "--quiet", "origin")
    if done.returncode != 0:
        raise Failed(f"fetch of origin failed: {tail(done.stderr)}")


def pin_main(root: Path) -> str:
    main = git_out(root, "rev-parse", "--verify", "refs/remotes/origin/main^{commit}").strip()
    if not _TREE_OID.fullmatch(main):
        raise Failed("origin/main could not be pinned")
    return main


def current_branch(root: Path) -> str:
    done = git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    if done.returncode != 0:
        raise Refused("the checkout is on a detached HEAD")
    return done.stdout.decode().strip()


def refuse_in_progress(root: Path) -> None:
    for marker in ("MERGE_HEAD", "rebase-merge", "rebase-apply"):
        done = git(root, "rev-parse", "--git-path", marker)
        if done.returncode == 0 and (root / done.stdout.decode().strip()).exists():
            raise Refused(f"an in-progress merge or rebase ({marker}) blocks the local branch")


def ensure_clean(root: Path) -> None:
    done = git(root, "status", "--porcelain=v1", "--untracked-files=all")
    if done.returncode != 0:
        raise Refused("the checkout state could not be measured")
    if done.stdout.strip():
        raise Refused("the checkout is dirty; commit or clean it first")


# ---------------------------------------------------------------------------
# The committed protection policy — never the candidate's own code.
# ---------------------------------------------------------------------------


def committed_runner_held(root: Path) -> tuple[str, ...]:
    """`RUNNER_HELD` as the invoking commit declares it (read, never executed)."""
    source = git_out(root, "show", "HEAD:scripts/stage2.py")
    try:
        module = ast.parse(source)
    except SyntaxError as error:
        raise Failed(f"committed scripts/stage2.py cannot be read as Python ({error})") from error
    for node in module.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "RUNNER_HELD" for target in node.targets
        ):
            if not isinstance(node.value, ast.Tuple | ast.List) or not node.value.elts:
                raise Failed("committed scripts/stage2.py declares no readable RUNNER_HELD tuple")
            parts = []
            for element in node.value.elts:
                if not isinstance(element, ast.Constant) or not isinstance(element.value, str):
                    raise Failed("committed scripts/stage2.py declares a non-string RUNNER_HELD entry")
                parts.append(element.value)
            return tuple(parts)
    raise Failed("committed scripts/stage2.py declares no RUNNER_HELD")


def committed_decided_prefixes(root: Path) -> list[str]:
    """Prefixes the committed provenance map reserves to human decisions."""
    try:
        data = yaml.safe_load(git_out(root, "show", "HEAD:provenance.yaml"))
    except yaml.YAMLError as error:
        raise Failed(f"the committed provenance.yaml cannot be read ({error})") from error
    if not isinstance(data, dict):
        raise Failed("the committed provenance.yaml is not a mapping")
    entries = data.get("paths")
    if entries is None:
        return []
    if not isinstance(entries, list):
        raise Failed("the committed provenance.yaml has no readable paths list")
    decided: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("prefix"), str):
            raise Failed("the committed provenance.yaml has an entry without a string prefix")
        allowed = entry.get("allowed")
        if isinstance(allowed, list) and allowed and set(allowed) == {"human-decided"}:
            decided.append(entry["prefix"])
    return decided


def held_prefixes(root: Path) -> list[str]:
    """Case-folded protection prefixes, exactly the runner's own two sources."""
    held = [*committed_decided_prefixes(root), *committed_runner_held(root)]
    return [prefix.casefold() for prefix in held]


def path_is_held(path: str, held: list[str]) -> bool:
    folded = path.casefold()
    return any(folded.startswith(prefix) for prefix in held)


# ---------------------------------------------------------------------------
# Pull-request discovery over `gh`.
# ---------------------------------------------------------------------------


def run_gh(gh: str, root: Path, *args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run([gh, *args], cwd=root, capture_output=True, timeout=GH_SECONDS, check=False)
    except subprocess.TimeoutExpired as error:
        raise Failed(f"gh {' '.join(args[:2])} did not finish within {GH_SECONDS} seconds") from error
    except OSError as error:
        raise Failed(f"gh could not be started: {error}") from error


def _iso_datetime(value: object, field_name: str) -> dt.datetime:
    if not isinstance(value, str):
        raise MetadataError(f"{field_name} is not a string")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise MetadataError(f"{field_name} is not a readable time") from error
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.UTC)
    return parsed.astimezone(dt.UTC)


def _string(item: dict, field_name: str) -> str:
    value = item.get(field_name)
    if not isinstance(value, str) or not value:
        raise MetadataError(f"{field_name} is absent or not a string")
    return value


def parse_pull(item: object) -> Pull:
    if not isinstance(item, dict):
        raise MetadataError("the pull request entry is not an object")
    number = item.get("number")
    if not isinstance(number, int) or isinstance(number, bool):
        raise MetadataError("number is absent or not an integer")
    head = _string(item, "headRefOid")
    if not _TREE_OID.fullmatch(head):
        raise MetadataError("headRefOid is not a commit id")
    cross = item.get("isCrossRepository")
    if not isinstance(cross, bool):
        raise MetadataError("isCrossRepository is absent or not a boolean")
    labels_raw = item.get("labels")
    if not isinstance(labels_raw, list):
        raise MetadataError("labels is absent or not a list")
    labels = []
    for entry in labels_raw:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
            raise MetadataError("a label is not an object with a name")
        labels.append(entry["name"])
    files_raw = item.get("files")
    if not isinstance(files_raw, list):
        raise MetadataError("files is absent or not a list")
    files: list[str] = []
    for entry in files_raw:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise MetadataError("a changed file is not an object with a path")
        files.append(entry["path"])
        previous = entry.get("previous_path")
        if previous is not None:
            if not isinstance(previous, str):
                raise MetadataError("a renamed file's previous_path is not a string")
            files.append(previous)
    return Pull(
        number=number,
        url=_string(item, "url"),
        title=_string(item, "title"),
        created=_iso_datetime(item.get("createdAt"), "createdAt"),
        base=_string(item, "baseRefName"),
        branch=_string(item, "headRefName"),
        head=head,
        cross_repository=cross,
        labels=labels,
        files=files,
    )


def discover(gh: str, root: Path) -> list[Pull]:
    """Every open pull request, paginated reads included; failure is an error."""
    done = run_gh(gh, root, "pr", "list", "--state", "open", "--json", LIST_FIELDS, "--paginate")
    if done.returncode != 0:
        raise Failed(f"pull-request discovery failed: {tail(done.stderr)}")
    text = done.stdout.decode("utf-8", "replace")
    if not text.strip():
        raise Failed("pull-request discovery gave no answer")
    decoder = json.JSONDecoder()
    pages: list[object] = []
    position = 0
    try:
        while position < len(text):
            while position < len(text) and text[position].isspace():
                position += 1
            if position >= len(text):
                break
            page, position = decoder.raw_decode(text, position)
            pages.append(page)
    except json.JSONDecodeError as error:
        raise Failed(f"pull-request discovery returned output that is not JSON ({error})") from error
    pulls: dict[int, Pull] = {}
    for page in pages:
        if not isinstance(page, list):
            raise Failed("pull-request discovery returned output that is not a JSON list")
        for item in page:
            try:
                pull = parse_pull(item)
            except MetadataError as error:
                raise Failed(f"pull-request discovery returned malformed metadata: {error}") from error
            pulls.setdefault(pull.number, pull)
    return [pulls[number] for number in sorted(pulls)]


def re_read(gh: str, root: Path, number: int) -> tuple[Pull, str]:
    """The pull request as it stands immediately before publishing."""
    done = run_gh(gh, root, "pr", "view", str(number), "--json", VIEW_FIELDS)
    if done.returncode != 0:
        raise Failed(f"the pull-request re-read failed: {tail(done.stderr)}")
    try:
        item = json.loads(done.stdout.decode("utf-8", "replace"))
    except json.JSONDecodeError as error:
        raise Failed(f"the pull-request re-read returned output that is not JSON ({error})") from error
    if not isinstance(item, dict):
        raise Failed("the pull-request re-read returned no object")
    pull = parse_pull(item)
    state = item.get("state")
    if not isinstance(state, str):
        raise MetadataError("state is absent or not a string")
    return pull, state


# ---------------------------------------------------------------------------
# Local checkouts of a target branch.
# ---------------------------------------------------------------------------


def branch_checkouts(root: Path, branch: str) -> list[tuple[Path, str]]:
    """Every worktree of `root` that has `branch` checked out, with its HEAD."""
    out = git_out(root, "worktree", "list", "--porcelain", "-z")
    found: list[tuple[Path, str]] = []
    records: list[dict[str, str]] = []
    # With -z every attribute is its own NUL-terminated field and a record ends
    # on an empty field; a `worktree` field opens the next record.
    for attribute in out.split("\0"):
        key, _, value = attribute.partition(" ")
        if key == "worktree":
            records.append({})
        if key and records:
            records[-1][key] = value
    for fields in records:
        if fields.get("branch") == f"refs/heads/{branch}":
            found.append((Path(fields["worktree"]), fields.get("HEAD", "")))
    return found


def checkout_problem(root: Path, branch: str, expected: str) -> str | None:
    """Why a local checkout of the branch forbids a push; None when none does."""
    for path, head in branch_checkouts(root, branch):
        status = git(path, "status", "--porcelain=v1", "--untracked-files=all")
        if status.returncode != 0:
            raise Failed(f"the checkout at {path} could not be inspected")
        if status.stdout.strip():
            return f"local checkout is dirty at {path}"
        try:
            count = int(git_out(root, "rev-list", "--count", f"{expected}..{head}").strip())
        except Failed as error:
            raise Failed(f"the checkout at {path} could not be inspected ({error})") from error
        if count > 0:
            return f"local checkout has unpushed commits at {path} ({count})"
    return None


# ---------------------------------------------------------------------------
# The shared merge engine: merged tree in, regenerated index in, commit out.
# ---------------------------------------------------------------------------


def merge_tree(root: Path, head: str, main_tip: str) -> tuple[str, list[str]]:
    """The merged tree of head and main, and the paths that truly conflict.

    `git merge-tree --write-tree -z` prints the tree OID, then per conflicted
    path a `<mode> <oid> <stage>` record with the path, then informational
    messages. Exit 1 means conflicts, not execution failure.
    """
    done = git(root, "merge-tree", "--write-tree", "-z", head, main_tip)
    if done.returncode not in (0, 1):
        raise Failed(f"git merge-tree failed ({done.returncode}): {tail(done.stderr)}")
    text = done.stdout.decode("utf-8", "replace")
    tree = text.split("\0", 1)[0].strip()
    if not _TREE_OID.fullmatch(tree):
        raise Failed("git merge-tree wrote no readable tree")
    conflicts: set[str] = set()
    if done.returncode == 1:
        for match in _CONFLICT_ENTRY.finditer(text):
            conflicts.add(match.group(1))
        if not conflicts:
            raise Failed("git merge-tree reported conflicts but named none that could be read")
    return tree, sorted(conflicts)


class Render:
    """The committed renderer run against one tree's plans inputs, in private.

    The mirror holds the merged tree's `plans/` as real files and `code`'s
    `scripts/` as the code - the fetched `origin/main` in both commands, so the
    index is rendered by the renderer the pushed branch's gate runs, never by an
    older checkout (review row L1-10), and never by candidate pull-request code — the scratch-mirror pattern of
    `stage2.trusted_registry`, with the data narrowed to the one directory the
    renderer reads. Writes stay inside the scratch holder; the renderer runs
    with a private HOME and TMPDIR and a preset-but-absent tracker render, so
    no candidate program, hook or tracker write can occur.
    """

    def __init__(self, root: Path, tree: str, code: str = "HEAD") -> None:
        self._holder = Path(tempfile.mkdtemp(prefix="pr-sync-render-"))
        try:
            self.mirror = self._holder / "mirror"
            (self.mirror / "plans").mkdir(parents=True)
            plans = git(root, "archive", "--format=tar", tree, "plans")
            if plans.returncode != 0:
                raise Failed(f"the merged plans tree could not be materialised: {tail(plans.stderr)}")
            self._extract(plans.stdout, self.mirror / "plans", "plans")
            scripts = git(root, "archive", "--format=tar", code, "scripts")
            if scripts.returncode != 0:
                raise Failed(f"the committed scripts could not be materialised: {tail(scripts.stderr)}")
            self._extract(scripts.stdout, self.mirror / "scripts", "scripts")
            self._validate()
        except BaseException:
            self.close()
            raise

    def _extract(self, archive: bytes, target: Path, top: str) -> None:
        try:
            with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
                for member in tar.getmembers():
                    if member.isdir():
                        continue
                    if not member.isfile():
                        raise Failed(f"the tree holds a non-regular entry {member.name}; refusing to materialise it")
                    relative = PurePosixPath(member.name)
                    if relative.is_absolute() or ".." in relative.parts:
                        raise Failed(f"the tree entry {member.name} would escape the scratch mirror")
                    parts = relative.parts[1:] if relative.parts[:1] == (top,) else relative.parts
                    destination = target.joinpath(*parts)
                    extracted = tar.extractfile(member)
                    if extracted is None:
                        raise Failed(f"the tree entry {member.name} could not be read")
                    try:
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        destination.write_bytes(extracted.read())
                    except OSError as error:
                        # A file where the tree needs a directory, or the reverse (review row L1-7).
                        raise Failed(f"the tree entry {member.name} cannot be materialised ({error})") from error
        except tarfile.TarError as error:
            raise Failed(f"the tree archive could not be read ({error})") from error

    def _validate(self) -> None:
        """Every artefact the renderer consumes has readable frontmatter and no
        unresolved conflict markers; otherwise the run refuses to render."""
        for path in sorted((self.mirror / "plans").rglob("*.md")):
            if path.name == "INDEX.md" or path.name.startswith("_"):
                continue
            rel = path.relative_to(self.mirror).as_posix()
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as error:
                raise Failed(f"{rel}: cannot be read ({error})") from error
            if not text.startswith("---\n"):
                raise Failed(f"{rel}: no readable frontmatter")
            end = text.find("\n---", 4)
            if end == -1:
                raise Failed(f"{rel}: no readable frontmatter")
            try:
                meta = yaml.safe_load(text[4:end])
            except yaml.YAMLError:
                raise Failed(f"{rel}: no readable frontmatter") from None
            if not isinstance(meta, dict):
                raise Failed(f"{rel}: no readable frontmatter")
            fence: str | None = None
            for line in text.splitlines():
                stripped = line.lstrip()
                marker = stripped[:3] if stripped[:3] in ("```", "~~~") else None
                if marker is not None:
                    # A marker quoted in a fenced example is text, not a conflict (review row L1-11).
                    fence = None if fence == marker else (fence or marker)
                    continue
                if fence is None and (line.startswith("<<<<<<< ") or line.startswith(">>>>>>> ")):
                    raise Failed(f"{rel}: unresolved conflict markers")

    def run(self) -> bytes:
        scratch = self._holder / "scratch"
        (scratch / "home").mkdir(parents=True, exist_ok=True)
        (scratch / "tmp").mkdir(parents=True, exist_ok=True)
        env = {
            **os.environ,
            "HOME": str(scratch / "home"),
            "TMPDIR": str(scratch / "tmp"),
            "BEAD_RENDER": str(scratch / "absent-issues.jsonl"),
        }
        try:
            done = subprocess.run(
                [sys.executable, str(self.mirror / "scripts" / "plans_registry.py"), "--index"],
                cwd=self.mirror,
                env=env,
                capture_output=True,
                timeout=RENDER_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            raise Failed(f"the committed renderer did not finish within {RENDER_SECONDS} seconds") from error
        except OSError as error:
            raise Failed(f"the committed renderer could not be started: {error}") from error
        if done.returncode != 0:
            raise Failed(f"the committed renderer exited {done.returncode}: {tail(done.stderr)}")
        index = self.mirror / "plans" / "INDEX.md"
        if not index.is_file():
            raise Failed("the committed renderer wrote no plans/INDEX.md")
        return index.read_bytes()

    def close(self) -> None:
        shutil.rmtree(self._holder, ignore_errors=True)

    def __enter__(self) -> Render:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def tree_entry(root: Path, tree: str, path: str) -> str | None:
    done = git(root, "rev-parse", "--verify", "--quiet", f"{tree}:{path}")
    if done.returncode != 0:
        return None
    return done.stdout.decode().strip()


def committed_index(root: Path, tree: str) -> bytes | None:
    done = git(root, "cat-file", "blob", f"{tree}:{INDEX_PATH}")
    return done.stdout if done.returncode == 0 else None


def render_tree(root: Path, tree: str) -> bytes | None:
    """The committed renderer's output for a tree; None when it has no plans/."""
    if tree_entry(root, tree, "plans") is None:
        return None
    with Render(root, tree) as render:
        return render.run()


def is_current(root: Path, head: str) -> bool:
    """Whether the committed index equals a fresh render of the same tree."""
    tree = git_out(root, "rev-parse", f"{head}^{{tree}}").strip()
    committed = committed_index(root, tree)
    if tree_entry(root, tree, "plans") is None:
        return committed is None
    return committed == render_tree(root, tree)


def build_commit(root: Path, tree: str, parents: list[str], message: str) -> str:
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "pr-sync",
        "GIT_AUTHOR_EMAIL": "pr-sync@invalid",
        "GIT_COMMITTER_NAME": "pr-sync",
        "GIT_COMMITTER_EMAIL": "pr-sync@invalid",
    }
    argv = ["commit-tree", tree]
    for parent in parents:
        argv += ["-p", parent]
    argv += ["-m", message]
    done = git(root, *argv, env=env)
    if done.returncode != 0:
        raise Failed(f"the merge commit could not be created: {tail(done.stderr)}")
    oid = done.stdout.decode().strip()
    if not _TREE_OID.fullmatch(oid):
        raise Failed("the merge commit could not be read back")
    return oid


def prepare_merge(root: Path, branch: str, head: str, main_tip: str, *, two_parent: bool) -> Prepared:
    """Build the merge (or repair) commit with a regenerated index; publish nothing."""
    if two_parent:
        merged, conflicts = merge_tree(root, head, main_tip)
        others = [path for path in conflicts if path != INDEX_PATH]
        if others:
            raise Conflict(paths=sorted(conflicts))
        if tree_entry(root, merged, "plans") is None:
            oid = build_commit(
                root, merged, [head, main_tip], f"Merge origin/main into {branch}\n\nNo plans tree to regenerate."
            )
            return Prepared(oid, f"merged origin/main ({main_tip})")
        with Render(root, merged, main_tip) as render:
            index_bytes = render.run()
        tree = tree_with_regenerated_index(root, merged, index_bytes)
        oid = build_commit(
            root,
            tree,
            [head, main_tip],
            f"Merge origin/main into {branch}\n\n"
            "plans/INDEX.md is regenerated from the merged plans tree by scripts/pr_sync.py, "
            "never taken from the merge result.",
        )
        return Prepared(oid, f"merged origin/main ({main_tip}), regenerated {INDEX_PATH}")
    tree = git_out(root, "rev-parse", f"{head}^{{tree}}").strip()
    with Render(root, tree, main_tip) as render:
        index_bytes = render.run()
    regenerated = tree_with_regenerated_index(root, tree, index_bytes)
    oid = build_commit(
        root,
        regenerated,
        [head],
        f"Regenerate {INDEX_PATH}\n\nRendered from the branch's own plans tree by scripts/pr_sync.py.",
    )
    return Prepared(oid, f"regenerated {INDEX_PATH}")


class Conflict(Exception):
    """A conflict outside the index; the target stays where it is."""

    def __init__(self, paths: list[str]) -> None:
        super().__init__(", ".join(paths))
        self.paths = paths


def tree_with_regenerated_index(root: Path, tree: str, index_bytes: bytes) -> str:
    """Insert the rendered index blob, keeping every other merged entry."""
    plans_tree = tree_entry(root, tree, "plans")
    if plans_tree is None:
        return tree
    blob_done = git(root, "hash-object", "-w", "--stdin", data=index_bytes)
    if blob_done.returncode != 0:
        raise Failed("the rendered index could not be stored as a blob")
    blob = blob_done.stdout.decode().strip()
    if not _TREE_OID.fullmatch(blob):
        raise Failed("the rendered index blob could not be read back")

    index_env = {**os.environ, "GIT_INDEX_FILE": str(Path(tempfile.mkdtemp(prefix="pr-sync-index-")) / "index")}
    try:
        done = git(root, "read-tree", plans_tree, env=index_env)
        if done.returncode != 0:
            raise Failed("the merged plans tree could not be loaded for regeneration")
        done = git(root, "update-index", "--add", "--cacheinfo", f"100644,{blob},INDEX.md", env=index_env)
        if done.returncode != 0:
            raise Failed("the rendered index could not replace the merged one")
        new_plans = git_out(root, "write-tree", env=index_env).strip()
    finally:
        shutil.rmtree(Path(index_env["GIT_INDEX_FILE"]).parent, ignore_errors=True)
    if not _TREE_OID.fullmatch(new_plans):
        raise Failed("the regenerated plans tree could not be read back")

    entries = git(root, "ls-tree", "-z", tree).stdout
    replaced = False
    rebuilt = bytearray()
    for entry in entries.split(b"\0"):
        if not entry:
            continue
        name = entry.split(b"\t", 1)[1] if b"\t" in entry else b""
        if name == b"plans":
            mode, _, rest = entry.partition(b" ")
            rebuilt += mode + b" tree " + new_plans.encode() + b"\tplans\0"
            replaced = True
        else:
            rebuilt += entry + b"\0"
    if not replaced:
        raise Failed("the merged tree holds no plans entry to replace")
    done = git(root, "mktree", "-z", data=bytes(rebuilt))
    if done.returncode != 0:
        raise Failed("the regenerated root tree could not be written")
    new_root = done.stdout.decode().strip()
    if not _TREE_OID.fullmatch(new_root):
        raise Failed("the regenerated root tree could not be read back")
    return new_root


# ---------------------------------------------------------------------------
# Publishing.
# ---------------------------------------------------------------------------


def remote_head(root: Path, branch: str) -> str | None:
    done = git(root, "ls-remote", "origin", f"refs/heads/{branch}")
    if done.returncode != 0:
        raise Failed(f"the remote head of {branch} could not be read: {tail(done.stderr)}")
    out = done.stdout.decode().strip()
    if not out:
        return None
    return out.split()[0]


def publish(root: Path, gh: str, pull: Pull, prepared: Prepared, held: list[str]) -> tuple[str, str]:
    """Re-measure everything immediately before the push, then push under a lease."""
    fresh, state = re_read(gh, root, pull.number)
    if state != "OPEN":
        return "outside scope", "the pull request is no longer open"
    reason = classify_skip(fresh, held)
    if reason is not None:
        return "protected", reason
    if fresh.head != pull.head:
        return "moved", f"the pull-request head moved during the run ({pull.head[:12]} -> {fresh.head[:12]})"
    actual = remote_head(root, pull.branch)
    if actual is None:
        raise Failed("the remote branch is gone before publishing")
    if actual != pull.head:
        return "moved", f"the remote head moved during the run ({pull.head[:12]} -> {actual[:12]})"
    problem = checkout_problem(root, pull.branch, actual)
    if problem is not None:
        return "protected", problem
    if not is_ancestor(root, pull.head, prepared.oid):
        raise Failed("the prepared commit no longer contains the inspected head; refusing to publish")
    detail = prepared.detail
    if branch_checkouts(root, pull.branch):
        detail += "; the local checkout must fast-forward"
    push = git(
        root,
        "-c",
        "core.hooksPath=/dev/null",
        "push",
        f"--force-with-lease=refs/heads/{pull.branch}:{pull.head}",
        "origin",
        f"{prepared.oid}:refs/heads/{pull.branch}",
    )
    if push.returncode != 0:
        raise Failed(f"the push to {pull.branch} was rejected: {tail(push.stderr)}")
    return "updated", detail


def is_ancestor(root: Path, older: str, newer: str) -> bool:
    return git(root, "merge-base", "--is-ancestor", older, newer).returncode == 0


# ---------------------------------------------------------------------------
# Classification and reporting.
# ---------------------------------------------------------------------------


def classify_skip(pull: Pull, held: list[str]) -> str | None:
    """Why the pull request must not be updated; None when it is eligible."""
    if pull.cross_repository:
        return "outside scope: fork pull request"
    if pull.base != "main":
        return f"outside scope: base '{pull.base}' is not main"
    if any(label.casefold() == "decision" for label in pull.labels):
        return "protected: decision pull request (label: decision)"
    if pull.title.startswith("decide("):
        return "protected: decision pull request (title starts with decide()"
    hits = sorted({path for path in pull.files if path_is_held(path, held)})
    if hits:
        return "protected: runner-held or human-decided paths: " + ", ".join(hits)
    return None


def working_days_after(created: dt.date, today: dt.date) -> int:
    """UTC weekdays strictly after the creation date through today."""
    days = 0
    day = created + dt.timedelta(days=1)
    while day <= today:
        if day.weekday() < 5:
            days += 1
        day += dt.timedelta(days=1)
    return days


def report(outcomes: list[tuple[Pull, str, str]], pulls: list[Pull], today: dt.date) -> None:
    print(f"sync report for {len(pulls)} open pull request(s):")
    for pull, kind, detail in outcomes:
        print(f"  {kind}: #{pull.number} {pull.url} — {detail}")
    overdue = [pull for pull in pulls if working_days_after(pull.created.date(), today) > WORKING_DAYS_OVERDUE]
    heading = f"overdue (older than {WORKING_DAYS_OVERDUE} working days)"
    if not overdue:
        print(f"{heading}: none")
        return
    print(f"{heading}:")
    for pull in overdue:
        age = working_days_after(pull.created.date(), today)
        print(f"#{pull.number} {pull.url} — {age} working days, listed whatever its protection")


def exit_code_for(kinds: list[str]) -> int:
    bad = {"conflict", "error", "moved"}
    return 1 if any(kind in bad for kind in kinds) else 0


# ---------------------------------------------------------------------------
# The two commands.
# ---------------------------------------------------------------------------


def merge_main(root: Path) -> int:
    try:
        ensure_repo(root)
    except Refused as error:
        print(f"refused: {error}")
        return 2
    try:
        fetch_origin(root)
        main_tip = pin_main(root)
        branch = current_branch(root)
        if branch == "main":
            raise Refused("merge-main refuses the main branch itself")
        refuse_in_progress(root)
        ensure_clean(root)
        head = git_out(root, "rev-parse", "HEAD").strip()
    except Refused as error:
        print(f"refused: {error}")
        return 2
    except Failed as error:
        print(f"error: {error}")
        return 1

    try:
        if is_ancestor(root, main_tip, head):
            if is_current(root, head):
                print(f"unchanged: {branch} — main is already merged and the index is current")
                return 0
            prepared = prepare_merge(root, branch, head, main_tip, two_parent=False)
        else:
            prepared = prepare_merge(root, branch, head, main_tip, two_parent=True)
    except Conflict as conflict:
        print(f"conflict: {branch} — conflicting paths: {', '.join(conflict.paths)}")
        print("the branch was not updated; resolve the conflict and merge again")
        return 1
    except Failed as error:
        print(f"error: {error}")
        return 1

    try:
        # Recheck immediately before the fast-forward; never reset user work.
        if current_branch(root) != branch or git_out(root, "rev-parse", "HEAD").strip() != head:
            raise Failed("the checkout changed during the run; nothing was applied")
        ensure_clean(root)
        applied = git(root, "-c", "core.hooksPath=/dev/null", "merge", "--quiet", "--ff-only", prepared.oid)
        if applied.returncode != 0:
            raise Failed(f"the fast-forward to the prepared commit failed: {tail(applied.stderr)}")
    except (Failed, Refused) as error:
        print(f"error: {error}")
        return 1
    print(f"applied: {branch} — {prepared.detail} ({prepared.oid[:12]})")
    return 0


def sync_main(root: Path, gh: str, today: dt.date) -> int:
    try:
        ensure_repo(root)
        fetch_origin(root)
        main_tip = pin_main(root)
        held = held_prefixes(root)
        pulls = discover(gh, root)
    except Refused as error:
        print(f"refused: {error}")
        return 2
    except Failed as error:
        print(f"error: {error}")
        return 1
    if not pulls:
        print("no open pull requests")
        report([], pulls, today)
        return 0

    outcomes: list[tuple[Pull, str, str]] = []
    prepared: list[tuple[Pull, Prepared]] = []
    for pull in pulls:
        try:
            skip = classify_skip(pull, held)
            if skip is not None:
                outcomes.append((pull, *split_kind(skip)))
                continue
            branch_ref = git_out(root, "rev-parse", "--verify", f"refs/remotes/origin/{pull.branch}^{{commit}}").strip()
            if branch_ref != pull.head:
                outcomes.append(
                    (
                        pull,
                        "moved",
                        f"the fetched branch ({branch_ref[:12]}) differs from the pull-request head "
                        f"({pull.head[:12]}); nothing is pushed",
                    )
                )
                continue
            problem = checkout_problem(root, pull.branch, branch_ref)
            if problem is not None:
                outcomes.append((pull, *split_kind(problem)))
                continue
            if is_ancestor(root, main_tip, pull.head):
                if is_current(root, pull.head):
                    outcomes.append((pull, "unchanged", "main is already merged and the index is current"))
                    continue
                built = prepare_merge(root, pull.branch, pull.head, main_tip, two_parent=False)
            else:
                built = prepare_merge(root, pull.branch, pull.head, main_tip, two_parent=True)
            if not is_ancestor(root, pull.head, built.oid):
                raise Failed("the prepared commit does not contain the pull-request head")
            prepared.append((pull, built))
        except Conflict as conflict:
            outcomes.append((pull, "conflict", "conflicting paths: " + ", ".join(conflict.paths)))
        except (Failed, MetadataError) as error:
            outcomes.append((pull, "error", str(error)))

    for pull, built in prepared:
        try:
            kind, detail = publish(root, gh, pull, built, held)
            outcomes.append((pull, kind, detail))
        except (Failed, MetadataError) as error:
            outcomes.append((pull, "error", str(error)))

    report(outcomes, pulls, today)
    return exit_code_for([kind for _, kind, _ in outcomes])


def split_kind(detail: str) -> tuple[str, str]:
    """Split a reason that already names its kind ('protected: ...')."""
    for kind in ("outside scope", "protected", "conflict", "error", "moved", "updated", "unchanged"):
        if detail.startswith(kind + ":"):
            return kind, detail[len(kind) + 1 :].strip()
    return "protected", detail


def parse_now(value: str | None) -> dt.date:
    if value is None:
        return dt.datetime.now(dt.UTC).date()
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"--now is not a readable ISO date or datetime: {value} ({error})") from None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.UTC)
    return parsed.astimezone(dt.UTC).date()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pr_sync.py",
        description="One supported merge that regenerates plans/INDEX.md, and an on-request sync for pull-request branches.",
        allow_abbrev=False,
    )
    commands = parser.add_subparsers(dest="command", required=True, metavar="{merge-main,sync}")
    merge = commands.add_parser(
        "merge-main",
        help="merge origin/main into the current branch, regenerating plans/INDEX.md; never pushes",
        description=(
            "Merge the fetched origin/main into the current branch of --root and fast-forward to the "
            "prepared result. For a hand merge and for preparing phase 6. Refuses a detached HEAD, main "
            "itself, an in-progress merge or rebase, and a dirty checkout."
        ),
        allow_abbrev=False,
    )
    merge.add_argument("--root", default=".", help="the worktree to merge in (default: .)")
    sync = commands.add_parser(
        "sync",
        help="update eligible open pull-request branches with origin/main; run on request only",
        description=(
            "Discover every open pull request with gh and push a merge of origin/main with a regenerated "
            "plans/INDEX.md to each eligible branch. Skips and reports forks, other bases, decision pull "
            "requests, runner-held or human-decided paths, and dirty or unpushed local checkouts. Never "
            "merges a pull request into main, never writes main."
        ),
        allow_abbrev=False,
    )
    sync.add_argument("--root", default=".", help="the worktree whose origin is measured (default: .)")
    sync.add_argument("--gh", default="gh", help="the gh executable; a stand-in may be injected for offline tests")
    sync.add_argument(
        "--now",
        default=None,
        help="override the UTC clock with an ISO date or datetime, for offline tests",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if args.command == "merge-main":
        return merge_main(root)
    try:
        return sync_main(root, args.gh, parse_now(args.now))
    except ValueError as error:
        print(f"pr_sync.py: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
