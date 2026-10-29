"""Offline regressions for the supported merge and the on-request sync.

`scripts/pr_sync.py` carries two commands: `merge-main` prepares the current
branch for a hand merge or phase 6, `sync` updates eligible pull-request
branches on explicit request. Both share one merge engine whose rule is the
change's name: the merged tree is rendered, never either parent's index
(plans/changes/index-merge-regenerates, beads coding-harness-hfsz,
coding-harness-njtm, coding-harness-eq6y).

Every test here runs against a real miniature repository of its own — a bare
origin, a work clone, branches that really merge — and a scripted `gh` stand-in
that paginates and can fail. No live GitHub call, no push outside the fixture.
The committed renderer of a fixture is a small deterministic stand-in of
`scripts/plans_registry.py --index`; `_render` is its twin, so assertions
compare the published index against a fresh render of the merged inputs.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PR_SYNC = REPO_ROOT / "scripts" / "pr_sync.py"

# The protection policy a fixture commits: its own `scripts/stage2.py` declares
# the held prefixes exactly the way the runner's module does, because the helper
# reads that tuple from the invoking committed tree.
FAKE_STAGE2 = 'RUNNER_HELD = (\n    "prompts/",\n    "templates/",\n    ".github/",\n)\n'
FAKE_PROVENANCE = 'schema_version: 1\npaths:\n  - prefix: "docs/adr/"\n    allowed: [human-decided]\n'

# The committed renderer of a fixture: deterministic, no tracker, no YAML — it
# renders one row per artefact from the `bead:` line of its frontmatter.
FAKE_RENDERER = """#!/usr/bin/env python3
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
plans = root / "plans"


def bead(path):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return "None"
    if not text.startswith("---\\n"):
        return "None"
    end = text.find("\\n---", 4)
    if end == -1:
        return "None"
    for line in text[4:end].splitlines():
        if line.startswith("bead:"):
            return line.split(":", 1)[1].strip() or "None"
    return "None"


rows = []
if plans.is_dir():
    for path in sorted(plans.rglob("*.md")):
        if path.name == "INDEX.md" or path.name.startswith("_"):
            continue
        rows.append(f"{path.relative_to(plans).as_posix()} {bead(path)}")
(plans / "INDEX.md").write_text("\\n".join(rows) + "\\n", encoding="utf-8")
print("written")
"""

FAILING_RENDERER = "#!/usr/bin/env python3\nimport sys\nsys.exit(7)\n"


def _git(cwd: Path, *args: str, check: bool = True) -> str:
    done = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, check=False)
    if check and done.returncode:
        raise AssertionError(f"git -C {cwd} {' '.join(args)} failed: {done.stderr}")
    return done.stdout.strip()


def _render(rows: list[tuple[str, str]]) -> str:
    """The twin of the fixture renderer: one row per artefact, sorted by path."""
    lines = [f"{rel} {bead}" for rel, bead in sorted(rows)]
    return "\n".join(lines) + "\n"


def _artefact(title: str, bead: str) -> str:
    return f"---\ntitle: {title}\nstatus: draft\nimplementation_status: none\nbead: {bead}\n---\n\n# {title}\n"


@dataclass
class Pull:
    """One pull request as the stand-in reports it."""

    number: int
    branch: str
    head: str
    base: str = "main"
    title: str = "a change"
    created: str = "2026-10-20T10:00:00Z"
    cross_repository: bool = False
    labels: list[dict] = field(default_factory=list)
    files: list[dict] = field(default_factory=list)

    def as_json(self) -> dict:
        return {
            "number": self.number,
            "state": "OPEN",
            "url": f"https://github.invalid/o/r/pull/{self.number}",
            "title": self.title,
            "createdAt": self.created,
            "baseRefName": self.base,
            "headRefName": self.branch,
            "headRefOid": self.head,
            "isCrossRepository": self.cross_repository,
            "labels": self.labels,
            "files": self.files,
        }


class World:
    """A bare origin, a work clone, and the scripted `gh` stand-in."""

    def __init__(self, tmp_path: Path, renderer: str = FAKE_RENDERER) -> None:
        self.tmp = tmp_path
        self.origin = tmp_path / "origin.git"
        self.work = tmp_path / "work"
        self.advances = 0
        self.tmp.mkdir(parents=True, exist_ok=True)
        _git(self.tmp, "init", "--bare", "--initial-branch=main", "--quiet", "origin.git")
        _git(self.tmp, "clone", "--quiet", "origin.git", "work")
        _git(self.work, "config", "user.email", "test@example.invalid")
        _git(self.work, "config", "user.name", "Test")
        (self.work / "scripts").mkdir()
        (self.work / "scripts" / "stage2.py").write_text(FAKE_STAGE2, encoding="utf-8")
        (self.work / "scripts" / "plans_registry.py").write_text(renderer, encoding="utf-8")
        (self.work / "provenance.yaml").write_text(FAKE_PROVENANCE, encoding="utf-8")
        self.write_plans("alpha/spec.md", _artefact("Alpha", "alpha-1"))
        self.commit_index([("alpha/spec.md", "alpha-1")], "main base")
        _git(self.work, "push", "--quiet", "origin", "main")

    # -- fixture building ---------------------------------------------------

    def write_plans(self, rel: str, text: str) -> None:
        path = self.work / "plans" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def write_root(self, rel: str, text: str) -> None:
        path = self.work / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit_index(self, rows: list[tuple[str, str]], message: str) -> str:
        (self.work / "plans" / "INDEX.md").write_text(_render(rows), encoding="utf-8")
        _git(self.work, "add", "-A")
        _git(self.work, "commit", "--quiet", "-m", message)
        return _git(self.work, "rev-parse", "HEAD")

    def push(self, branch: str) -> str:
        _git(self.work, "push", "--quiet", "origin", f"{branch}:{branch}")
        return _git(self.origin, "rev-parse", f"refs/heads/{branch}")

    def checkout(self, name: str) -> None:
        _git(self.work, "checkout", "--quiet", name)

    def branch(self, name: str, start: str | None = None) -> None:
        """Create and check out a branch — from the current HEAD, or from `start`."""
        args = ["checkout", "--quiet", "-b", name] + ([start] if start else [])
        _git(self.work, *args)

    def commit_raw(self, message: str) -> str:
        """Commit the tree as it stands — for a deliberately stale index."""
        _git(self.work, "add", "-A")
        _git(self.work, "commit", "--quiet", "-m", message)
        return _git(self.work, "rev-parse", "HEAD")

    # -- the commands under test --------------------------------------------

    def run_sync(
        self, *extra: str, env: dict | None = None, pulls: list[Pull] | None = None
    ) -> subprocess.CompletedProcess:
        standin = self.write_gh()
        run_env = {**os.environ, **self.env_pulls(pulls or []), **(env or {})}
        return subprocess.run(
            [sys.executable, str(PR_SYNC), "sync", "--root", str(self.work), "--gh", str(standin), *extra],
            capture_output=True,
            text=True,
            env=run_env,
            cwd=self.tmp,
            timeout=300,
        )

    def run_merge_main(self, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(PR_SYNC), "merge-main", "--root", str(self.work), *extra],
            capture_output=True,
            text=True,
            cwd=self.tmp,
            timeout=300,
        )

    def write_gh(self) -> Path:
        """The stand-in: paginates `pr list` over the injected pulls and can fail or race."""
        standin = self.tmp / "gh-standin.py"
        script = """#!/usr/bin/env python3
import json
import os
import subprocess
import sys

prs = json.loads(os.environ.get("PR_SYNC_PRS", "[]"))
mode = os.environ.get("PR_SYNC_GH_MODE", "")
args = sys.argv[1:]
if mode == "fail-list" and "list" in args:
    sys.exit(3)
if "list" in args:
    if mode == "empty-list":
        sys.exit(0)
    if mode == "bad-list":
        print("this is not json")
        sys.exit(0)
    half = max(1, len(prs) // 2)
    print(json.dumps(prs[:half]))
    print(json.dumps(prs[half:]))
    sys.exit(0)
if "view" in args:
    if mode == "fail-view":
        sys.exit(3)
    number = args[args.index("view") + 1]
    race = os.environ.get("PR_SYNC_RACE_CMD", "")
    if race:
        subprocess.run(json.loads(race), check=True, capture_output=True)
    for pr in prs:
        if str(pr["number"]) == number:
            print(json.dumps(pr))
            sys.exit(0)
    sys.exit(1)
sys.exit(9)
"""
        standin.write_text(script, encoding="utf-8")
        standin.chmod(0o755)
        return standin

    def env_pulls(self, pulls: list[Pull]) -> dict:
        return {"PR_SYNC_PRS": json.dumps([pull.as_json() for pull in pulls])}

    # -- assertions ----------------------------------------------------------

    def origin_ref(self, ref: str) -> str | None:
        done = _git(self.origin, "rev-parse", "--verify", "--quiet", ref, check=False)
        return done or None

    def origin_index(self, branch: str) -> str:
        """The pushed index byte for byte — `_git` would strip the trailing newline."""
        head = self.origin_ref(f"refs/heads/{branch}")
        done = subprocess.run(
            ["git", "-C", str(self.origin), "show", f"{head}:plans/INDEX.md"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert done.returncode == 0, done.stderr
        return done.stdout

    def all_origin_heads(self) -> dict[str, str]:
        out = _git(self.origin, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads/")
        return dict(line.split(" ") for line in out.splitlines())

    def advance_main(self, rows: list[tuple[str, str]], rel: str | None = None, title: str | None = None) -> str:
        """Advance main with one new artefact and a fresh index. A second call
        on the same World takes its own fresh artefact, so every advance stays
        a real commit."""
        n = self.advances
        self.advances += 1
        if rel is None:
            stem = "delta" if n == 0 else f"delta{n + 1}"
            rel, title = f"{stem}/spec.md", stem.capitalize()
        title = title or rel.split("/")[-1].removesuffix(".md").capitalize()
        self.checkout("main")
        self.write_plans(rel, _artefact(title, title.lower()))
        if all(name != rel for name, _ in rows):
            rows = [*rows, (rel, title.lower())]
        head = self.commit_index(rows, "main advances")
        _git(self.work, "push", "--quiet", "origin", "main")
        return head

    def add_worktree(self, path: Path, branch: str) -> None:
        _git(self.work, "fetch", "--quiet", "origin")
        _git(self.work, "worktree", "add", "--quiet", str(path), branch)


# ---------------------------------------------------------------------------
# Criterion 1 — the supported local merge renders the complete merged tree.
# ---------------------------------------------------------------------------


def test_merge_renders_all_merged_inputs(tmp_path: Path) -> None:
    """Neither parent's index survives: even Git's clean textual merge of the
    index is replaced by a fresh render of the merged artefacts."""
    world = World(tmp_path)
    world.branch("feat/union")
    world.write_plans("gamma/plan.md", _artefact("Gamma", "gamma-1"))
    # The branch's own index is left stale: textually identical to base main's,
    # so the three-way merge of the index is clean — and wrong without a render.
    branch_head = world.commit_raw("branch adds gamma, forgets the index")
    world.push("feat/union")
    main_tip = world.advance_main([("alpha/spec.md", "alpha-1"), ("delta/spec.md", "delta")])

    world.checkout("feat/union")
    done = world.run_merge_main()
    assert done.returncode == 0, done.stdout + done.stderr
    merged = _render(
        [
            ("alpha/spec.md", "alpha-1"),
            ("delta/spec.md", "delta"),
            ("gamma/plan.md", "gamma-1"),
        ]
    )
    assert (world.work / "plans" / "INDEX.md").read_text(encoding="utf-8") == merged
    assert "gamma/plan.md" in merged and "delta/spec.md" in merged, "either parent's artefact went missing"
    assert _git(world.work, "rev-parse", "HEAD^1") == branch_head, "the pull-request head is not the first parent"
    assert _git(world.work, "rev-parse", "HEAD^2") == main_tip, "fetched main is not the second parent"
    # A local merge never pushes.
    assert world.origin_ref("refs/heads/feat/union") == branch_head


def test_index_only_conflict_is_regenerated(tmp_path: Path) -> None:
    """A conflict confined to plans/INDEX.md is resolved by regeneration, not
    by a textual resolution."""
    world = World(tmp_path)
    world.branch("feat/idxconf")
    hand_edited = world.commit_index(
        [("alpha/spec.md", "alpha-1"), ("zzz/spec.md", "zzz-1")], "branch hand-edits the index"
    )
    world.push("feat/idxconf")
    main_tip = world.advance_main([("alpha/spec.md", "alpha-1"), ("delta/spec.md", "delta")])

    world.checkout("feat/idxconf")
    done = world.run_merge_main()
    assert done.returncode == 0, done.stdout + done.stderr
    merged = _render([("alpha/spec.md", "alpha-1"), ("delta/spec.md", "delta")])
    assert (world.work / "plans" / "INDEX.md").read_text(encoding="utf-8") == merged
    assert "zzz" not in merged and "<<<<<<<" not in merged
    assert _git(world.work, "rev-parse", "HEAD^1") == hand_edited
    assert _git(world.work, "rev-parse", "HEAD^2") == main_tip


def test_other_conflicts_preserve_target(tmp_path: Path) -> None:
    """A conflict outside the index is reported with its paths; neither the
    branch ref nor the checked-out work moves."""
    world = World(tmp_path)
    world.branch("feat/clash")
    world.write_root("docs/guide.md", "branch line\n")
    clash_head = world.commit_raw("branch writes the guide")
    world.push("feat/clash")
    world.advance_main([("alpha/spec.md", "alpha-1"), ("delta/spec.md", "delta")])
    world.write_root("docs/guide.md", "main line\n")
    world.commit_raw("main writes the guide differently")
    _git(world.work, "push", "--quiet", "origin", "main")

    world.checkout("feat/clash")
    index_before = (world.work / "plans" / "INDEX.md").read_bytes()
    done = world.run_merge_main()
    assert done.returncode == 1, done.stdout + done.stderr
    assert "docs/guide.md" in done.stdout, "the conflicting paths were not named"
    assert _git(world.work, "rev-parse", "HEAD") == clash_head, "the target branch moved despite the conflict"
    assert (world.work / "plans" / "INDEX.md").read_bytes() == index_before
    assert world.origin_ref("refs/heads/feat/clash") == clash_head


# ---------------------------------------------------------------------------
# Criterion 4 — `make index` is the existing generator, pinned by behaviour.
# ---------------------------------------------------------------------------


def test_make_index_uses_existing_generator(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The Makefile target runs the plans-index generator, and both render
    paths produce the same bytes from the same small fixture."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import plans_registry as reg  # noqa: PLC0415 — the real generator, imported once here

    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    assert "index" in makefile.split(".PHONY:")[1].splitlines()[0], "the index target is not .PHONY"
    recipe = None
    started = False
    for line in makefile.splitlines():
        if line == "index:":
            started = True
        elif started and line.startswith("\t"):
            recipe = line.strip()
            break
        elif started:
            break
    assert recipe == "@python3 scripts/plans_registry.py --index", "make index no longer runs the generator"

    fixture = tmp_path / "mkfix"
    (fixture / "plans" / "one").mkdir(parents=True)
    (fixture / "scripts").mkdir()
    (fixture / "plans" / "one" / "spec.md").write_text(_artefact("One", "bead-1"), encoding="utf-8")
    (fixture / "plans" / "two.md").write_text(_artefact("Two", "bead-2"), encoding="utf-8")
    for name in ("plans_registry.py", "_verdict.py"):
        shutil.copy(REPO_ROOT / "scripts" / name, fixture / "scripts" / name)

    env = {**os.environ, "PATH": f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}"}
    via_make = subprocess.run(
        ["make", "-C", str(fixture), "-f", str(REPO_ROOT / "Makefile"), "index"],
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )
    assert via_make.returncode == 0, via_make.stderr
    from_make = (fixture / "plans" / "INDEX.md").read_bytes()

    (fixture / "plans" / "INDEX.md").write_text("stale\n", encoding="utf-8")
    direct = subprocess.run(
        [sys.executable, "scripts/plans_registry.py", "--index"],
        capture_output=True,
        text=True,
        cwd=fixture,
        timeout=120,
    )
    assert direct.returncode == 0, direct.stderr
    from_direct = (fixture / "plans" / "INDEX.md").read_bytes()

    assert from_make == from_direct, "the two render paths disagree on the same inputs"
    monkeypatch.setattr(reg, "REPO", fixture)
    monkeypatch.setattr(reg, "PLANS", fixture / "plans")
    monkeypatch.setattr(reg, "INDEX", fixture / "plans" / "INDEX.md")
    assert from_make.decode("utf-8") == reg.render_index(), "neither path equals the generator's own render"


# ---------------------------------------------------------------------------
# Criteria 5, 6 — the sync publishes measured merges and reports real conflicts.
# ---------------------------------------------------------------------------


def test_sync_pushes_clean_and_index_only_merges(tmp_path: Path) -> None:
    """An eligible branch behind main gets a merge that keeps its head as the
    first parent, includes the main tip, and carries the regenerated index."""
    world = World(tmp_path)
    world.branch("feat/clean")
    world.write_plans("gamma/plan.md", _artefact("Gamma", "gamma-1"))
    clean_head = world.commit_raw("clean branch")
    world.push("feat/clean")
    # From main, not from feat/clean: the hand-edited-index branch must not
    # inherit the clean branch's gamma artefact.
    world.branch("feat/idxconf2", start="main")
    idxconf_head = world.commit_index([("alpha/spec.md", "alpha-1"), ("zzz/spec.md", "zzz-1")], "hand-edited index")
    world.push("feat/idxconf2")
    main_tip = world.advance_main([("alpha/spec.md", "alpha-1"), ("delta/spec.md", "delta")])

    pulls = [
        Pull(7, "feat/clean", clean_head, files=[{"path": "plans/gamma/plan.md"}]),
        Pull(9, "feat/idxconf2", idxconf_head, files=[{"path": "plans/INDEX.md"}]),
    ]
    done = world.run_sync(pulls=pulls)
    assert done.returncode == 0, done.stdout + done.stderr

    clean_pushed = world.origin_ref("refs/heads/feat/clean")
    assert clean_pushed not in (None, clean_head), "the clean branch was not updated"
    assert _git(world.origin, "rev-parse", f"{clean_pushed}^1") == clean_head, "pull-request ancestry was lost"
    assert _git(world.origin, "rev-parse", f"{clean_pushed}^2") == main_tip
    expected = _render(
        [
            ("alpha/spec.md", "alpha-1"),
            ("delta/spec.md", "delta"),
            ("gamma/plan.md", "gamma-1"),
        ]
    )
    assert world.origin_index("feat/clean") == expected, "the pushed index is not a render of the merged tree"

    idxconf_pushed = world.origin_ref("refs/heads/feat/idxconf2")
    assert idxconf_pushed not in (None, idxconf_head)
    assert _git(world.origin, "rev-parse", f"{idxconf_pushed}^1") == idxconf_head
    pushed_index = world.origin_index("feat/idxconf2")
    assert pushed_index == _render([("alpha/spec.md", "alpha-1"), ("delta/spec.md", "delta")])
    assert "zzz" not in pushed_index and "<<<<<<<" not in pushed_index
    assert world.origin_ref("refs/heads/main") == main_tip, "the sync wrote main"


def test_sync_reports_conflicting_paths_without_push(tmp_path: Path) -> None:
    """An ordinary conflict leaves the branch ref untouched and names its paths."""
    world = World(tmp_path)
    world.branch("feat/clash")
    world.write_root("docs/guide.md", "branch line\n")
    clash_head = world.commit_raw("branch writes the guide")
    world.push("feat/clash")
    world.advance_main([("alpha/spec.md", "alpha-1"), ("delta/spec.md", "delta")])
    world.write_root("docs/guide.md", "main line\n")
    world.commit_raw("main writes the guide differently")
    _git(world.work, "push", "--quiet", "origin", "main")

    pull = Pull(6, "feat/clash", clash_head, files=[{"path": "docs/guide.md"}])
    done = world.run_sync(pulls=[pull])
    assert done.returncode == 1, done.stdout + done.stderr
    assert "docs/guide.md" in done.stdout, "the report does not name the conflicting paths"
    assert world.origin_ref("refs/heads/feat/clash") == clash_head, "the branch changed remotely despite the conflict"


# ---------------------------------------------------------------------------
# Criterion 7 — protected pull requests are reported, never merged into.
# ---------------------------------------------------------------------------


def test_sync_skips_protected_work(tmp_path: Path) -> None:
    """Decision, runner-held, human-decided, dirty-worktree and unpushed
    worktree cases are each reported with their reason; no ref moves."""
    world = World(tmp_path)
    world.advance_main([("alpha/spec.md", "alpha-1"), ("delta/spec.md", "delta")])

    def pushed_branch(name: str) -> str:
        world.branch(name)
        world.write_plans(f"{name.split('/')[-1]}/spec.md", _artefact(name, f"bead-{name}"))
        head = world.commit_raw(name)
        world.push(name)
        return head

    decision_head = pushed_branch("feat/decision")
    title_head = pushed_branch("feat/decidable")
    held_head = pushed_branch("feat/held")
    world.branch("feat/held2")
    world.write_root("docs/adr/0001-recorded.md", "# an ADR\n")
    decided_head = world.commit_raw("changes a human-decided path")
    world.push("feat/held2")
    dirty_head = pushed_branch("feat/dirty")
    unpushed_head = pushed_branch("feat/unpushed")

    pulls = [
        Pull(3, "feat/decision", decision_head, labels=[{"name": "decision"}]),
        Pull(4, "feat/decidable", title_head, title="decide(gates): move a day"),
        Pull(5, "feat/held", held_head, files=[{"path": "prompts/06-review.md"}]),
        Pull(6, "feat/held2", decided_head, files=[{"path": "docs/adr/0001-recorded.md"}]),
        Pull(8, "feat/dirty", dirty_head),
        Pull(13, "feat/unpushed", unpushed_head),
    ]

    # Off the branches: `worktree add` refuses a branch another checkout
    # already holds, and the worktrees — not the clone — must hold the
    # protection here.
    world.checkout("main")

    dirty = tmp_path / "wt-dirty"
    world.add_worktree(dirty, "feat/dirty")
    (dirty / "scratch.txt").write_text("uncommitted\n", encoding="utf-8")
    unpushed = tmp_path / "wt-unpushed"
    world.add_worktree(unpushed, "feat/unpushed")
    (unpushed / "plans" / "unpushed/spec.md").parent.mkdir(parents=True, exist_ok=True)
    (unpushed / "plans" / "unpushed" / "spec.md").write_text(_artefact("Local", "local-1"), encoding="utf-8")
    _git(unpushed, "add", "-A")
    _git(unpushed, "commit", "--quiet", "-m", "work not on its remote branch")

    before = world.all_origin_heads()
    done = world.run_sync(pulls=pulls)
    assert done.returncode == 0, done.stdout + done.stderr + "protected skips alone are not errors"
    for number, reason in (
        (3, "decision"),
        (4, "decide("),
        (5, "prompts/06-review.md"),
        (6, "docs/adr/0001-recorded.md"),
        (8, "dirty"),
        (13, "unpushed"),
    ):
        assert f"#{number}" in done.stdout, f"pull request #{number} disappeared from the report"
        assert reason in done.stdout, f"the reason for #{number} is not named"
    assert world.all_origin_heads() == before, "a protected branch was updated"


# ---------------------------------------------------------------------------
# Criterion 8 — an undeterminable state is an error, never permission to push.
# ---------------------------------------------------------------------------


def test_uncertain_sync_state_never_pushes(tmp_path: Path) -> None:
    """Failed discovery, fetch, metadata, policy read or publish re-read each
    leave every branch unchanged and turn the run red."""
    cases: list[tuple[str, callable]] = []

    def case_fail_list(base: Path) -> tuple[World, list[Pull], dict, str]:
        world = World(base)
        head = _branch_behind(world, "feat/behind")
        pull = Pull(7, "feat/behind", head)
        return world, [pull], {"PR_SYNC_GH_MODE": "fail-list"}, "discovery"

    def case_empty_list(base: Path) -> tuple[World, list[Pull], dict, str]:
        world = World(base)
        head = _branch_behind(world, "feat/behind")
        return world, [Pull(7, "feat/behind", head)], {"PR_SYNC_GH_MODE": "empty-list"}, "no answer"

    def case_bad_list(base: Path) -> tuple[World, list[Pull], dict, str]:
        world = World(base)
        head = _branch_behind(world, "feat/behind")
        return world, [Pull(7, "feat/behind", head)], {"PR_SYNC_GH_MODE": "bad-list"}, "JSON"

    def case_fail_view(base: Path) -> tuple[World, list[Pull], dict, str]:
        world = World(base)
        head = _branch_behind(world, "feat/behind")
        return world, [Pull(7, "feat/behind", head)], {"PR_SYNC_GH_MODE": "fail-view"}, "re-read"

    def case_fetch(base: Path) -> tuple[World, list[Pull], dict, str]:
        world = World(base)
        head = _branch_behind(world, "feat/behind")
        _git(world.work, "remote", "set-url", "origin", str(base / "missing.git"))
        return world, [Pull(7, "feat/behind", head)], {}, "fetch"

    def case_bad_provenance(base: Path) -> tuple[World, list[Pull], dict, str]:
        world = World(base)
        world.checkout("main")
        (world.work / "provenance.yaml").write_text("paths: [ { prefix: [unclosed\n", encoding="utf-8")
        world.commit_raw("breaks the provenance map")
        _git(world.work, "push", "--quiet", "origin", "main")
        head = _branch_behind(world, "feat/behind")
        return world, [Pull(7, "feat/behind", head)], {}, "provenance"

    def case_no_policy(base: Path) -> tuple[World, list[Pull], dict, str]:
        world = World(base)
        world.checkout("main")
        (world.work / "scripts" / "stage2.py").write_text("x = 1\n", encoding="utf-8")
        world.commit_raw("drops the held-prefix tuple")
        _git(world.work, "push", "--quiet", "origin", "main")
        head = _branch_behind(world, "feat/behind")
        return world, [Pull(7, "feat/behind", head)], {}, "RUNNER_HELD"

    cases = [
        ("stand-in refuses the listing", case_fail_list),
        ("stand-in answers nothing", case_empty_list),
        ("stand-in answers garbage", case_bad_list),
        ("stand-in refuses the re-read", case_fail_view),
        ("fetch fails", case_fetch),
        ("provenance unreadable", case_bad_provenance),
        ("held prefixes absent", case_no_policy),
    ]
    for index, (name, build) in enumerate(cases):
        world, pulls, env, expected_word = build(tmp_path / f"case-{index}")
        before = world.all_origin_heads()
        done = world.run_sync(pulls=pulls, env=env)
        assert done.returncode == 1, f"{name}: the run passed an undeterminable state\n{done.stdout}"
        assert expected_word in done.stdout + done.stderr, f"{name}: the failure is not named"
        assert world.all_origin_heads() == before, f"{name}: a branch moved anyway"


def _branch_behind(world: World, name: str) -> str:
    """An eligible branch: pushed from the base main, behind a later advance."""
    world.branch(name)
    world.write_plans("gamma/plan.md", _artefact("Gamma", "gamma-1"))
    head = world.commit_raw("a clean branch")
    world.push(name)
    world.advance_main([("alpha/spec.md", "alpha-1"), ("delta/spec.md", "delta")])
    return head


# ---------------------------------------------------------------------------
# Criterion 9 — a racing writer's commit is left intact and reported.
# ---------------------------------------------------------------------------


def test_moved_remote_head_is_preserved(tmp_path: Path) -> None:
    """If the remote head moves after inspection, the sync refuses to push and
    reports the move; the other writer's commit stays."""
    world = World(tmp_path)
    race_head = _branch_behind(world, "feat/race")

    world.checkout("main")
    world.write_plans("epsilon/spec.md", _artefact("Epsilon", "epsilon-1"))
    world.commit_index([("alpha/spec.md", "alpha-1"), ("epsilon/spec.md", "epsilon-1")], "a second writer arrives")
    racing_sha = _git(world.work, "rev-parse", "HEAD")
    _git(world.work, "push", "--quiet", "origin", "main:refs/races/next")

    race_cmd = json.dumps(["git", "-C", str(world.origin), "update-ref", "refs/heads/feat/race", racing_sha])
    done = world.run_sync(pulls=[Pull(9, "feat/race", race_head)], env={"PR_SYNC_RACE_CMD": race_cmd})
    assert done.returncode == 1, done.stdout + done.stderr
    assert "moved: #9" in done.stdout, "the race was not reported for the pull request"
    assert world.origin_ref("refs/heads/feat/race") == racing_sha, "the other writer's commit was overwritten"


# ---------------------------------------------------------------------------
# Criterion 10 — the overdue list counts UTC working days, protection aside.
# ---------------------------------------------------------------------------


def test_overdue_report_counts_weekdays(tmp_path: Path) -> None:
    first = dt.date(2026, 10, 5)
    monday = first - dt.timedelta(days=first.weekday())
    assert monday.weekday() == 0, "the fixture needs a Monday"

    world = World(tmp_path)
    head = _branch_behind(world, "feat/decision")
    pull = Pull(3, "feat/decision", head, labels=[{"name": "decision"}], created=f"{monday.isoformat()}T10:00:00Z")

    sixth = world.run_sync("--now", (monday + dt.timedelta(days=8)).isoformat(), pulls=[pull])
    assert sixth.returncode == 0, sixth.stdout + sixth.stderr
    assert "overdue" in sixth.stdout and "#3" in sixth.stdout, "the sixth working day was omitted"

    fifth = world.run_sync("--now", (monday + dt.timedelta(days=7)).isoformat(), pulls=[pull])
    assert fifth.returncode == 0
    assert "#3" not in _overdue_lines(fifth.stdout), "the fifth working day was already called overdue"

    world2 = World(tmp_path / "weekend")
    weekend_head = _branch_behind(world2, "feat/weekend")
    weekend = Pull(
        4,
        "feat/weekend",
        weekend_head,
        labels=[{"name": "decision"}],
        created=f"{(monday + dt.timedelta(days=4)).isoformat()}T10:00:00Z",
    )
    after_weekend = world2.run_sync("--now", (monday + dt.timedelta(days=7)).isoformat(), pulls=[weekend])
    assert after_weekend.returncode == 0
    assert "#4" not in _overdue_lines(after_weekend.stdout), "a weekend increased the age"


def _overdue_lines(report: str) -> list[str]:
    lines = report.splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith("overdue")), None)
    if start is None:
        return []
    return [line for line in lines[start + 1 :] if line.startswith("#")]


# ---------------------------------------------------------------------------
# Criterion 11 — forks and other bases are outside the update scope.
# ---------------------------------------------------------------------------


def test_sync_does_not_update_forks_or_other_bases(tmp_path: Path) -> None:
    world = World(tmp_path)
    fork_head = _branch_behind(world, "feat/forked")
    base_head = _branch_behind(world, "feat/elsewhere")
    before = world.all_origin_heads()

    pulls = [
        Pull(11, "feat/forked", fork_head, cross_repository=True),
        Pull(12, "feat/elsewhere", base_head, base="release-1"),
    ]
    done = world.run_sync(pulls=pulls)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "outside scope" in done.stdout
    assert "fork" in done.stdout and "release-1" in done.stdout, "the out-of-scope reasons are not named"
    assert world.all_origin_heads() == before, "an out-of-scope branch received a push"


# ---------------------------------------------------------------------------
# Criterion 12 — a measured pass repeats as unchanged.
# ---------------------------------------------------------------------------


def test_repeated_merge_and_sync_are_unchanged(tmp_path: Path) -> None:
    world = World(tmp_path)
    behind_head = _branch_behind(world, "feat/behind")
    main_tip = world.origin_ref("refs/heads/main")
    # A branch created after the advance: main is its ancestor, its index is current.
    world.branch("feat/current")
    world.write_plans("gamma/plan.md", _artefact("Gamma", "gamma-1"))
    current_head = world.commit_index(
        [
            ("alpha/spec.md", "alpha-1"),
            ("delta/spec.md", "delta"),
            ("gamma/plan.md", "gamma-1"),
        ],
        "a branch that already contains main",
    )
    world.push("feat/current")

    world.checkout("feat/behind")
    first = world.run_merge_main()
    assert first.returncode == 0, first.stdout + first.stderr
    after_merge = _git(world.work, "rev-parse", "HEAD")
    assert after_merge != behind_head
    second = world.run_merge_main()
    assert second.returncode == 0, second.stdout + second.stderr
    assert "unchanged" in second.stdout, "the second merge was not measured as unchanged"
    assert _git(world.work, "rev-parse", "HEAD") == after_merge, "the second merge moved the branch"
    # Off the branch: a local checkout with unpushed commits would protect it,
    # and the sync must then refuse — these branches are meant to be pushed.
    world.checkout("main")

    pull = Pull(12, "feat/current", current_head)
    run_one = world.run_sync(pulls=[pull])
    assert run_one.returncode == 0, run_one.stdout + run_one.stderr
    assert world.origin_ref("refs/heads/feat/current") == current_head, "a current branch was pushed anyway"

    behind = Pull(7, "feat/behind", behind_head)
    updated = world.run_sync(pulls=[pull, behind])
    assert updated.returncode == 0, updated.stdout + updated.stderr
    pushed = world.origin_ref("refs/heads/feat/behind")
    assert pushed != behind_head and pushed is not None
    assert world.origin_ref("refs/heads/feat/current") == current_head
    assert _git(world.origin, "rev-parse", f"{pushed}^2") == main_tip

    # The second run sees the pushed merge as the pull-request's head — the
    # stand-in's data moves with the push, as the real gh would.
    run_two = world.run_sync(pulls=[pull, Pull(7, "feat/behind", pushed)])
    assert run_two.returncode == 0, run_two.stdout + run_two.stderr
    assert world.origin_ref("refs/heads/feat/behind") == pushed, "the second sync pushed again"
    assert world.origin_ref("refs/heads/feat/current") == current_head
    assert run_two.stdout.count("unchanged") >= 2, "the repeated sync did not measure both branches as unchanged"


# ---------------------------------------------------------------------------
# Criterion 13 — failed generation or bad merged inputs publish nothing.
# ---------------------------------------------------------------------------


def test_bad_merged_inputs_or_renderer_preserve_target(tmp_path: Path) -> None:
    world = World(tmp_path)
    world.advance_main([("alpha/spec.md", "alpha-1"), ("delta/spec.md", "delta")])

    # Each fault on its own branch from main, so neither merged tree inherits
    # the other's artefact and each report names its own bad input.
    world.branch("feat/markers")
    world.write_plans("mk/spec.md", _artefact("Markers", "mk-1") + "<<<<<<< ours\n")
    markers_head = world.commit_raw("an artefact carrying conflict markers")
    world.push("feat/markers")

    world.branch("feat/badfm", start="main")
    world.write_plans("bad/spec.md", "---\nbead: [unclosed\n---\n")
    badfm_head = world.commit_raw("an artefact with unreadable frontmatter")
    world.push("feat/badfm")

    pulls = [
        Pull(13, "feat/badfm", badfm_head, files=[{"path": "plans/bad/spec.md"}]),
        Pull(14, "feat/markers", markers_head, files=[{"path": "plans/mk/spec.md"}]),
    ]
    before = world.all_origin_heads()
    done = world.run_sync(pulls=pulls)
    assert done.returncode == 1, done.stdout + done.stderr
    assert "bad/spec.md" in done.stdout and "mk/spec.md" in done.stdout, "the bad inputs are not named"
    assert world.all_origin_heads() == before, "a branch was updated despite failed generation"

    failing = World(tmp_path / "renderer", renderer=FAILING_RENDERER)
    failing.advance_main([("alpha/spec.md", "alpha-1"), ("delta/spec.md", "delta")])
    behind_head = _branch_behind(failing, "feat/behind")
    pull = Pull(15, "feat/behind", behind_head)
    done = failing.run_sync(pulls=[pull])
    assert done.returncode == 1, done.stdout + done.stderr
    assert failing.origin_ref("refs/heads/feat/behind") == behind_head

    failing.checkout("feat/behind")
    done = failing.run_merge_main()
    assert done.returncode == 1, done.stdout + done.stderr
    assert _git(failing.work, "rev-parse", "HEAD") == behind_head, "a failed renderer still produced a target update"


# ---------------------------------------------------------------------------
# Criterion 15 — the registry gate still blocks a stale index, writing nothing.
# ---------------------------------------------------------------------------

FULL_ARTEFACT = (
    "---\ntitle: Alpha\nstatus: draft\nimplementation_status: none\n"
    "date: 2026-10-28\nlast_reviewed: 2026-10-28\nbead: alpha-1\n---\n\n# Alpha\n"
)


def test_registry_still_blocks_without_repair(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A committed index that differs from its inputs is a BLOCK, and checking
    it leaves its bytes exactly as they were."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import plans_registry as reg  # noqa: PLC0415 — the gate under regression, imported once here

    root = tmp_path / "registry"
    (root / "plans").mkdir(parents=True)
    (root / ".beads").mkdir()
    (root / "plans" / "alpha").mkdir()
    (root / "plans" / "alpha" / "spec.md").write_text(FULL_ARTEFACT, encoding="utf-8")
    issues = root / ".beads" / "issues.jsonl"
    issues.write_text(json.dumps({"id": "alpha-1", "status": "open"}) + "\n", encoding="utf-8")

    monkeypatch.setattr(reg, "REPO", root)
    monkeypatch.setattr(reg, "PLANS", root / "plans")
    monkeypatch.setattr(reg, "INDEX", root / "plans" / "INDEX.md")
    monkeypatch.setattr(reg, "_bead_export_path", lambda: issues)

    current = reg.render_index()
    reg.INDEX.write_text(current, encoding="utf-8")
    healthy = reg.check()
    assert healthy.exit_code(strict=False) == 0, healthy.render()
    assert "deviates from its inputs" not in healthy.render()

    planted = current.replace("alpha/spec.md", "alpha/renamed.md")
    assert planted != current, "the fault was not planted"
    reg.INDEX.write_text(planted, encoding="utf-8")
    before = reg.INDEX.read_bytes()

    blocked = reg.check()
    assert blocked.exit_code(strict=False) != 0, "a stale index passed the gate"
    assert "deviates from its inputs" in blocked.render()
    assert reg.INDEX.read_bytes() == before, "checking repaired the index instead of measuring it"


# ---------------------------------------------------------------------------
# Review loop round 1 (2026-10-28): rows the orchestrator repaired by hand; each
# test was red on the code before its fix.
# ---------------------------------------------------------------------------


def _pr_sync():
    import importlib

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    return importlib.import_module("pr_sync")


def _repo(path: Path) -> Path:
    path.mkdir(parents=True)
    _git(path, "init", "--quiet", "--initial-branch=main")
    _git(path, "config", "user.email", "test@example.invalid")
    _git(path, "config", "user.name", "Test")
    return path


RENDERER_SAYING = """#!/usr/bin/env python3
from pathlib import Path

(Path(__file__).resolve().parent.parent / "plans" / "INDEX.md").write_text({!r}, encoding="utf-8")
"""


def test_a_decision_label_is_protected_in_any_case() -> None:
    """Row L1-15. Planted fault: a label `Decision` was treated as ordinary work."""
    m = _pr_sync()
    pull = m.Pull(
        number=1,
        url="https://github.invalid/o/r/pull/1",
        title="a change",
        created=dt.datetime(2026, 10, 20, tzinfo=dt.UTC),
        base="main",
        branch="feat/a",
        head="0" * 40,
        cross_repository=False,
        labels=["Decision"],
    )
    assert (m.classify_skip(pull, []) or "").startswith("protected: decision")


def test_a_plans_file_in_the_tree_is_a_reported_failure(tmp_path: Path) -> None:
    """Row L1-7. Planted fault: a regular file named `plans` crashed the run with IsADirectoryError."""
    m = _pr_sync()
    repo = _repo(tmp_path / "repo")
    (repo / "plans").write_text("not a directory\n", encoding="utf-8")
    (repo / "scripts").mkdir()
    (repo / "scripts" / "plans_registry.py").write_text(RENDERER_SAYING.format("x\n"), encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "--quiet", "-m", "a file where the plans tree belongs")
    tree = _git(repo, "rev-parse", "HEAD^{tree}")
    with pytest.raises(m.Failed):
        m.Render(repo, tree)


def test_a_fenced_conflict_marker_does_not_refuse_the_render(tmp_path: Path) -> None:
    """Row L1-11. Planted fault: a conflict marker quoted in a fenced example refused every merge."""
    m = _pr_sync()
    repo = _repo(tmp_path / "repo")
    (repo / "plans" / "x").mkdir(parents=True)
    (repo / "plans" / "x" / "plan.md").write_text(
        "---\ntitle: Plan\nbead: x-1\n---\n\n# Plan\n\n```text\n<<<<<<< ours\n=======\n>>>>>>> theirs\n```\n",
        encoding="utf-8",
    )
    (repo / "scripts").mkdir()
    (repo / "scripts" / "plans_registry.py").write_text(RENDERER_SAYING.format("index\n"), encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "--quiet", "-m", "a plan that quotes conflict markers")
    with m.Render(repo, _git(repo, "rev-parse", "HEAD^{tree}")) as render:
        assert render.run() == b"index\n"


def test_the_index_is_rendered_by_mains_scripts_not_the_checkout(tmp_path: Path) -> None:
    """Row L1-10. Planted fault: the operator's older checkout rendered the index the gate then rejects."""
    m = _pr_sync()
    repo = _repo(tmp_path / "repo")
    (repo / "plans" / "x").mkdir(parents=True)
    (repo / "plans" / "x" / "spec.md").write_text("---\ntitle: Spec\nbead: x-1\n---\n\n# Spec\n", encoding="utf-8")
    (repo / "scripts").mkdir()
    registry = repo / "scripts" / "plans_registry.py"
    registry.write_text(RENDERER_SAYING.format("old renderer\n"), encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "--quiet", "-m", "the older renderer")
    old = _git(repo, "rev-parse", "HEAD")
    registry.write_text(RENDERER_SAYING.format("main renderer\n"), encoding="utf-8")
    _git(repo, "commit", "--quiet", "-am", "main's renderer")
    main_tip = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "--quiet", "--detach", old)
    prepared = m.prepare_merge(repo, "feat/x", main_tip, main_tip, two_parent=False)
    assert _git(repo, "show", f"{prepared.oid}:plans/INDEX.md") == "main renderer"


def test_a_fetched_branch_that_differs_is_not_called_ahead(tmp_path: Path) -> None:
    """Rows L1-12, L1-14. Planted fault: a differing fetched branch was reported as ahead, with no ancestry measured."""
    world = World(tmp_path)
    world.branch("feat/x")
    world.write_plans("x/spec.md", _artefact("X", "x-1"))
    world.commit_index([("alpha/spec.md", "alpha-1"), ("x/spec.md", "x-1")], "a change")
    world.push("feat/x")
    other = world.origin_ref("refs/heads/main")
    done = world.run_sync(pulls=[Pull(7, "feat/x", other)])
    assert "differs from the pull-request head" in done.stdout, done.stdout
    assert "already ahead" not in done.stdout


def test_currency_is_judged_by_mains_renderer_not_the_checkout(tmp_path: Path) -> None:
    """Row L2-1. Planted fault: an index rendered by main's renderer was judged stale by an older checkout's."""
    m = _pr_sync()
    repo = _repo(tmp_path / "repo")
    (repo / "plans" / "x").mkdir(parents=True)
    (repo / "plans" / "x" / "spec.md").write_text("---\ntitle: Spec\nbead: x-1\n---\n\n# Spec\n", encoding="utf-8")
    (repo / "scripts").mkdir()
    registry = repo / "scripts" / "plans_registry.py"
    registry.write_text(RENDERER_SAYING.format("old renderer\n"), encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "--quiet", "-m", "the older renderer")
    old = _git(repo, "rev-parse", "HEAD")
    registry.write_text(RENDERER_SAYING.format("main renderer\n"), encoding="utf-8")
    (repo / "plans" / "INDEX.md").write_text("main renderer\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "--quiet", "-m", "main's renderer and the index it renders")
    main_tip = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "--quiet", "--detach", old)
    assert m.is_current(repo, main_tip, main_tip) is True
