"""The guarded merge-queue admission (plans/changes/enqueue-pr, bead coding-harness-va1l).

Every test builds its own history: a bare origin with `main` and the pull ref `refs/pull/7/head`, and a
checkout the command runs in. GitHub and the tracker are stand-ins; no test reaches a real queue.
"""

from __future__ import annotations

import dataclasses
import itertools
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import enqueue_pr as ep  # noqa: E402
import pr_sync  # noqa: E402

GIT = shutil.which("git")
REAL_SCRIPT = Path(ep.__file__).read_bytes()
FINDINGS = "plans/changes/demo/findings.md"
SPEC = "plans/changes/demo/spec.md"
VERDICT = "Phase 6 verdict: codex T1, 2026-11-25"
NO_FINDING = "Codex reported no finding."
FIXED = "fixed — tests/test_x.py::test_y"
HEADER = (
    "| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |\n"
    "|---|---|---|---|---|---|---|---|---|"
)
RELEASED_HEADER = (
    "| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |\n"
    "|---|---|---|---|---|---|---|---|---|---|"
)


def git(cwd: Path, *args: str) -> str:
    config = ("-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false")
    quiet = ("-c", "init.defaultBranch=main", "-c", "maintenance.auto=false", "-c", "gc.auto=0")
    result = subprocess.run([GIT, *config, *quiet, *args], cwd=cwd, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def spec(bead: str) -> str:
    return f"---\ntitle: Spec\nbead: {bead}\n---\n\n# Spec\n"


def table(*statuses: str) -> str:
    rows = [
        f"| F-{n} | MINOR | CODE | criterion 1 | src/app.py:{n} | finding {n} | Codex | {status} | — |"
        for n, status in enumerate(statuses, 1)
    ]
    return "\n".join([HEADER, *rows])


def released(*rows: tuple[str, str]) -> str:
    lines = [
        f"| L1-{n} | MAJOR | CODE | criterion 1 | src/app.py:{n} | loop finding {n} | m | {status} | — | {mark} |"
        for n, (status, mark) in enumerate(rows, 1)
    ]
    rows_table = "\n".join([RELEASED_HEADER, *lines])
    return "\n\n".join(["## Phase 4b — loop rows, released 2026-11-25", rows_table, "Rounds run: 1"])


def phase6(
    reviewed: str | None,
    *,
    body: str = NO_FINDING,
    verdict: str = VERDICT,
    earlier: str = "",
    after: str = "",
) -> str:
    """A findings.md whose last phase-6 block is the runner's shape: heading, body, reviewed commit, verdict."""
    parts = [earlier, "## Phase 6 — Codex, 2026-11-25", body]
    if reviewed:
        parts.append(f"Reviewed commit: {reviewed}")
    parts += [verdict, after]
    return "# Findings\n\n" + "\n\n".join(part for part in parts if part) + "\n"


@dataclass
class FakeGitHub:
    pr: ep.PullRequest
    required: set[str] = field(default_factory=lambda: {"verify"})
    states: list[tuple[str, str]] = field(default_factory=lambda: [("verify", "SUCCESS")])
    failing: set[str] = field(default_factory=set)
    enqueue_error: str | None = None
    head_after_error: str | None = None
    reread_fails: bool = False
    calls: list[tuple] = field(default_factory=list)

    def _called(self, name: str, *args: object) -> None:
        self.calls.append((name, *args))
        if name in self.failing:
            raise ep.Unreadable(f"gh {name} failed: HTTP 502")

    def pull_request(self, number: int) -> ep.PullRequest:
        reread = any(call[0] == "enqueue" for call in self.calls)
        self._called("pull_request", number)
        if reread and self.reread_fails:
            raise ep.Unreadable("gh api graphql failed: HTTP 502")
        if reread and self.head_after_error:
            return dataclasses.replace(self.pr, head_oid=self.head_after_error)
        return self.pr

    def required_checks(self, branch: str) -> set[str]:
        self._called("required_checks", branch)
        return set(self.required)

    def head_checks(self, oid: str) -> list[tuple[str, str]]:
        self._called("head_checks", oid)
        return list(self.states)

    def enqueue(self, node_id: str, head: str) -> dict:
        self._called("enqueue", node_id, head)
        if self.enqueue_error:
            raise ep.AdmissionError(self.enqueue_error)
        return {"position": 1, "state": "QUEUED"}

    def enqueued(self) -> list[tuple]:
        return [call[1:] for call in self.calls if call[0] == "enqueue"]

    def names(self) -> list[str]:
        return [call[0] for call in self.calls]


@dataclass
class World:
    root: Path
    origin: Path
    base: str
    main_tip: str
    reviewed: str
    head: str
    gh: FakeGitHub
    statuses: dict[str, str]
    tracker_error: str | None = None

    @property
    def script(self) -> Path:
        return self.root / "scripts" / "enqueue_pr.py"

    def tracker(self) -> dict[str, str]:
        if self.tracker_error:
            raise ep.Unreadable(self.tracker_error)
        return dict(self.statuses)

    def run(self, *argv: str) -> int:
        return ep.run(list(argv), root=self.root, github=self.gh, tracker=self.tracker, script=self.script)

    def commit(self, files: dict[str, str | bytes | None], message: str) -> str:
        write(self.root, files)
        git(self.root, "add", "-A")
        git(self.root, "commit", "--quiet", "--allow-empty", "-m", message)
        return git(self.root, "rev-parse", "HEAD")

    def publish(self) -> None:
        """The checkout's HEAD becomes the pull request's head, on origin and at GitHub."""
        git(self.root, "push", "--quiet", "--force", "origin", "HEAD:refs/pull/7/head")
        self.head = git(self.root, "rev-parse", "HEAD")
        self.gh.pr = dataclasses.replace(self.gh.pr, head_oid=self.head)


def write(root: Path, files: dict[str, str | bytes | None]) -> None:
    for name, content in files.items():
        path = root / name
        if content is None:
            path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")


DEFAULT_CHANGE = {SPEC: spec("demo-1"), "src/app.py": "value = 2\n"}
TRAILER = "Closes-Bead: demo-1"


def build(
    place: Path,
    *,
    change: dict[str, str | bytes | None] | None = None,
    record: Callable[[str, str], dict[str, str | bytes | None]] | None = None,
    trailers: tuple[str, ...] = (TRAILER,),
    main_ahead: bool = False,
    script_on_main: bool = True,
    statuses: dict[str, str] | None = None,
) -> World:
    """origin's main (the script, an index, the code), then the change, then the phase-6 record as the head."""
    place.mkdir(parents=True)
    origin = place / "origin.git"
    git(place, "init", "--quiet", "--bare", str(origin))
    root = place / "work"
    root.mkdir()
    git(root, "init", "--quiet")
    git(root, "remote", "add", "origin", str(origin))
    base_files: dict[str, str | bytes | None] = {"plans/INDEX.md": "# Index\n", "src/app.py": "value = 1\n"}
    base_files["provenance.yaml"] = "paths: []\n"
    base_files["scripts/enqueue_pr.py"] = REAL_SCRIPT if script_on_main else b"# another script\n"
    write(root, base_files)
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "-m", "base")
    base = git(root, "rev-parse", "HEAD")
    git(root, "push", "--quiet", "origin", "HEAD:refs/heads/main")
    main_tip = base
    if main_ahead:
        write(root, {"docs/main-note.md": "main moved\n"})
        git(root, "add", "docs/main-note.md")
        git(root, "commit", "--quiet", "-m", "main moves")
        git(root, "push", "--quiet", "origin", "HEAD:refs/heads/main")
        main_tip = git(root, "rev-parse", "HEAD")
    git(root, "checkout", "--quiet", "-b", "feat", base)
    if not script_on_main:
        (root / "scripts" / "enqueue_pr.py").write_bytes(REAL_SCRIPT)
    write(root, DEFAULT_CHANGE if change is None else change)
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "-m", "the change")
    reviewed = git(root, "rev-parse", "HEAD")
    files = record(reviewed, main_tip) if record else {FINDINGS: phase6(reviewed)}
    message = "record the phase-6 verdict" + ("\n\n" + "\n".join(trailers) if trailers else "")
    write(root, files)
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "--allow-empty", "-m", message)
    head = git(root, "rev-parse", "HEAD")
    git(root, "push", "--quiet", "origin", "HEAD:refs/pull/7/head")
    pr = ep.PullRequest(
        node_id="PR_node7",
        number=7,
        state="OPEN",
        is_draft=False,
        base="main",
        head_oid=head,
        cross_repository=False,
        in_merge_queue=False,
        labels=(),
    )
    known = {"demo-1": "in_progress", "demo-2": "open"} if statuses is None else statuses
    return World(root, origin, base, main_tip, reviewed, head, FakeGitHub(pr), known)


@pytest.fixture
def make(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Callable[..., World]:
    for key in list(os.environ):
        if key.startswith("GIT_"):
            monkeypatch.delenv(key)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    counter = itertools.count()

    def builder(**options: object) -> World:
        return build(tmp_path / f"world{next(counter)}", **options)  # type: ignore[arg-type]

    return builder


def refusal_lines(err: str) -> list[str]:
    return [line for line in err.splitlines() if not line.startswith("refused:")]


def refused(world: World, capsys: pytest.CaptureFixture[str], *argv: str) -> str:
    """Run, expect a refusal with nothing queued, and return stderr."""
    assert world.run("7", *argv) == 1
    assert world.gh.enqueued() == [], "a refused request reached the enqueue mutation"
    captured = capsys.readouterr()
    assert captured.err.startswith("refused: PR #7")
    assert captured.out == "", "a refusal reported on stdout"
    return captured.err


def admitted(world: World, capsys: pytest.CaptureFixture[str], *argv: str) -> str:
    code = world.run("7", *argv)
    captured = capsys.readouterr()
    assert code == 0, captured.err
    assert world.gh.enqueued() == [("PR_node7", world.head)]
    return captured.out


# ---------------------------------------------------------------------------
# Criteria 1 and 2: eligibility
# ---------------------------------------------------------------------------


def test_eligible_head_is_queued(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 1. Planted fault: an eligible head is refused or not queued."""
    world = make()
    out = admitted(world, capsys)
    assert out.startswith("queued: PR #7")
    # The counterpart: the same history with its required check failed is refused and not queued.
    failing = make()
    failing.gh.states = [("verify", "FAILURE")]
    refused(failing, capsys)


@pytest.mark.parametrize(
    "change",
    [{"state": "CLOSED"}, {"state": "MERGED"}, {"base": "release"}, {"is_draft": True}, {"cross_repository": True}],
    ids=["closed", "merged", "other-base", "draft", "fork"],
)
def test_ineligible_request_is_refused(
    make: Callable[..., World], capsys: pytest.CaptureFixture[str], change: dict
) -> None:
    """Criterion 2. Planted fault: a closed, other-branch, draft or fork request reaches admission."""
    world = make()
    world.gh.pr = dataclasses.replace(world.gh.pr, **change)
    err = refused(world, capsys)
    assert any(line.startswith("pr: ") for line in refusal_lines(err))


# ---------------------------------------------------------------------------
# Criteria 3, 22 and 23: the latest phase-6 verdict and the released loop rows
# ---------------------------------------------------------------------------

EARLIER_OPEN = f"## Phase 6 — Codex, 2026-11-20\n\n{table('open')}\n\nPhase 6 verdict: codex T0, 2026-11-20"
EARLIER_CLEAN = f"## Phase 6 — Codex, 2026-11-20\n\n{NO_FINDING}\n\nPhase 6 verdict: codex T0, 2026-11-20"

PHASE6_CASES = {
    "open-minor-row": (lambda r: phase6(r, body=table("open")), False),
    "taken-row": (lambda r: phase6(r, body=table(FIXED, "taken — repair it")), False),
    "divergent-row": (lambda r: phase6(r, body=table("[DIVERGENT]")), False),
    "settled-rows": (lambda r: phase6(r, body=table(FIXED, "rejected — out of scope")), True),
    "two-verdicts": (lambda r: phase6(r, verdict=f"{VERDICT}\n\nPhase 6 verdict: codex T2, 2026-11-25"), False),
    "no-verdict": (lambda r: phase6(r, verdict=""), False),
    "pending-verdict": (lambda r: phase6(r, verdict="Phase 6 verdict: pending"), False),
    "unrecognised-table-line": (lambda r: phase6(r, body=f"{NO_FINDING}\n\n| F-1 | MAJOR | open |"), False),
    "rows-and-no-finding": (lambda r: phase6(r, body=f"{table(FIXED)}\n\n{NO_FINDING}"), False),
    "earlier-open-latest-clean": (lambda r: phase6(r, earlier=EARLIER_OPEN), True),
    "earlier-clean-latest-open": (lambda r: phase6(r, earlier=EARLIER_CLEAN, body=table("open")), False),
    "no-phase-6-block": (lambda _r: "# Findings\n\nNothing reviewed yet.\n", False),
}


@pytest.mark.parametrize("status", ["fixed pending repair", "rejected until reviewed", "fixedness", "rejectedly"])
def test_unresolved_status_prefixes_refuse_admission(
    make: Callable[..., World], capsys: pytest.CaptureFixture[str], status: str
) -> None:
    world = make(record=lambda reviewed, _main: {FINDINGS: phase6(reviewed, body=table(status))})
    err = refused(world, capsys)
    assert "phase-6:" in err


@pytest.mark.parametrize(
    "status", ["fixed", "rejected", "fixed — proof", "rejected: reason", "fixed - proof", "rejected (reason)"]
)
def test_canonical_settled_statuses_are_accepted(status: str) -> None:
    assert ep.settled(status)


@pytest.mark.parametrize("case", list(PHASE6_CASES))
def test_latest_phase_six_is_settled(make: Callable[..., World], capsys: pytest.CaptureFixture[str], case: str) -> None:
    """Criterion 3. Planted fault: an absent, ambiguous, open, taken or unrecognised latest verdict is admitted,
    or a settled latest verdict after an open earlier one is refused."""
    render, expected = PHASE6_CASES[case]
    world = make(record=lambda reviewed, _main: {FINDINGS: render(reviewed)})
    if expected:
        admitted(world, capsys)
    else:
        err = refused(world, capsys)
        assert any(line.startswith("phase-6: ") for line in refusal_lines(err))
        if case == "no-phase-6-block":
            assert "reviewed-commit: not evaluated: phase-6" in err


@pytest.mark.parametrize(
    ("body", "expected"),
    [("", False), (f"> {NO_FINDING}", False), (f"  {NO_FINDING}", False), (NO_FINDING, True)],
    ids=["bare-verdict", "quoted", "indented", "runner-line"],
)
def test_no_finding_requires_unquoted_runner_statement(
    make: Callable[..., World], capsys: pytest.CaptureFixture[str], body: str, expected: bool
) -> None:
    """Criterion 22. Planted fault: a bare verdict or a quoted statement passes, or the runner's own line fails."""
    world = make(record=lambda reviewed, _main: {FINDINGS: phase6(reviewed, body=body)})
    if expected:
        admitted(world, capsys)
    else:
        err = refused(world, capsys)
        assert "phase-6: the block has no finding row and no unquoted" in err


@pytest.mark.parametrize(
    ("status", "mark", "expected"),
    [
        ("taken — repair it", "agree", False),
        ("open", "—", False),
        (FIXED, "disagree — the fix misses the case", False),
        (FIXED, "agree", True),
        ("rejected — an accepted limit", "no answer", False),
        (FIXED, "—", False),
    ],
    ids=["taken", "open", "disagreed", "fixed-agreed", "rejected", "missing-mark"],
)
def test_released_loop_rows_and_disagreements_refuse(
    make: Callable[..., World], capsys: pytest.CaptureFixture[str], status: str, mark: str, expected: bool
) -> None:
    """Criterion 23. Planted fault: an unsettled or disputed released loop row passes beside a no-finding verdict."""
    kept = "Kept from the loop record:\n\n> | L9-9 | MAJOR | x | y | z | w | m | open | — | — |"
    after = released((status, mark)) + "\n\n" + kept
    world = make(record=lambda reviewed, _main: {FINDINGS: phase6(reviewed, after=after)})
    if expected:
        admitted(world, capsys)
    else:
        err = refused(world, capsys)
        assert any(line.startswith("phase-6: ") and "L1-1" in line for line in refusal_lines(err))
        assert "L9-9" not in err, "a quoted kept line was read as a released row"


@pytest.mark.parametrize("missing", ["leading", "trailing"])
@pytest.mark.parametrize("section", ["phase6", "released"])
def test_malformed_table_rows_refuse_admission(
    make: Callable[..., World], capsys: pytest.CaptureFixture[str], missing: str, section: str
) -> None:
    row = "| F-1 | MAJOR | SPEC | criterion | file | symbol | open | open |"
    if section == "released":
        row = "| L1-1 | MAJOR | SPEC | criterion | file | symbol | open | open | — | agree |"
    malformed = row[1:] if missing == "leading" else row[:-1]
    body = f"{NO_FINDING}\n\n{malformed}" if section == "phase6" else NO_FINDING
    after = f"## Phase 4b — loop rows, released 2026-11-25\n\n{malformed}" if section == "released" else ""
    world = make(record=lambda reviewed, _main: {FINDINGS: phase6(reviewed, body=body, after=after)})
    assert "unrecognised table line" in refused(world, capsys)


def test_quoted_malformed_table_lines_are_ignored() -> None:
    quoted = "> F-1 | MAJOR | unresolved"
    assert not ep.phase6_problems(phase6("a" * 40, body=f"{NO_FINDING}\n\n{quoted}").splitlines())
    assert not ep.released_problems(f"## Phase 4b — loop rows, released\n\n{quoted}")


@pytest.mark.parametrize("mark", ["banana", "agreement", "agree pending", "agreed"])
def test_unrecognised_released_mark_refuses(mark: str) -> None:
    problems = ep.released_problems(released((FIXED, mark)))
    assert any("unrecognised" in problem and "L1-1" in problem for problem in problems)
    for valid in ("agree", "AGREE — reason", "agree: reason", "agree - reason", "agree (reason)"):
        assert not ep.released_problems(released((FIXED, valid)))


# ---------------------------------------------------------------------------
# Criteria 4 and 5: the trailer and the change folder
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("trailers", "statuses", "expected"),
    [
        ((), None, False),
        ((TRAILER, "Closes-Bead: demo-2"), None, False),
        (("Closes-Bead: demo-9",), None, False),
        ((TRAILER,), {"demo-1": "closed"}, False),
        (("closes-bead: demo-1",), None, False),
        ((TRAILER,), {"demo-1": "open"}, True),
    ],
    ids=["absent", "two", "unknown", "closed", "malformed-key", "open"],
)
def test_single_open_bead_trailer(
    make: Callable[..., World],
    capsys: pytest.CaptureFixture[str],
    trailers: tuple[str, ...],
    statuses: dict | None,
    expected: bool,
) -> None:
    """Criterion 4. Planted fault: an absent, multiple, unknown or closed declaration reaches admission."""
    world = make(trailers=trailers, statuses=statuses)
    if expected:
        admitted(world, capsys)
    else:
        err = refused(world, capsys)
        assert any(line.startswith("trailer: ") for line in refusal_lines(err))


def test_unique_changed_folder_matches_bead(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 5. Planted fault: zero, several or a mismatching change folder reaches admission."""
    none = make(
        change={"src/app.py": "value = 2\n"},
        record=lambda reviewed, _main: {"plans/notes/findings.md": phase6(reviewed)},
    )
    err = refused(none, capsys)
    assert "change: the diff touches 0 change folders; exactly one is required" in err
    assert "phase-6: not evaluated: change" in err

    several = make(change={**DEFAULT_CHANGE, "plans/changes/other/spec.md": spec("demo-1")})
    err = refused(several, capsys)
    assert "change: the diff touches 2 change folders: demo, other; exactly one is required" in err

    mismatch = make(change={**DEFAULT_CHANGE, SPEC: spec("demo-2")})
    err = refused(mismatch, capsys)
    assert "change: plans/changes/demo/ names bead demo-2; the head's Closes-Bead names demo-1" in err

    # An archived folder is no change folder of this pull request.
    archived = make(change={**DEFAULT_CHANGE, "plans/changes/archive/2026-10-01-old/spec.md": spec("old-1")})
    admitted(archived, capsys)


# ---------------------------------------------------------------------------
# Criteria 6 and 7: the reviewed commit and what follows it
# ---------------------------------------------------------------------------


def test_reviewed_commit_is_ancestor(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 6. Planted fault: a missing, unknown or unrelated reviewed commit reaches admission."""
    missing = make(record=lambda _reviewed, _main: {FINDINGS: phase6(None)})
    err = refused(missing, capsys)
    assert "reviewed-commit: the last phase-6 block names 0 reviewed commits; exactly one is required" in err
    assert "post-review: not evaluated: reviewed-commit" in err

    unrelated = make(main_ahead=True, record=lambda _reviewed, main: {FINDINGS: phase6(main)})
    err = refused(unrelated, capsys)
    assert f"reviewed-commit: the reviewed commit {unrelated.main_tip} is not an ancestor of the head" in err

    unknown = make(record=lambda _reviewed, _main: {FINDINGS: phase6("0" * 40)})
    err = refused(unknown, capsys)
    assert f"reviewed-commit: the reviewed commit {'0' * 40} could not be read" in err

    ancestor = make()
    admitted(ancestor, capsys)


def _merge(world: World, ref: str, message: str, *, alter: bool = False) -> None:
    if alter:
        git(world.root, "merge", "--quiet", "--no-ff", "--no-commit", ref)
        write(world.root, {"src/app.py": "value = 99\n"})
        git(world.root, "add", "-A")
        git(world.root, "commit", "--quiet", "-m", message)
    else:
        git(world.root, "merge", "--quiet", "--no-ff", "-m", message, ref)


def _side_branch(world: World) -> str:
    git(world.root, "checkout", "--quiet", "-b", "side", world.base)
    write(world.root, {"docs/side.md": "side\n"})
    git(world.root, "add", "-A")
    git(world.root, "commit", "--quiet", "-m", "side work")
    side = git(world.root, "rev-parse", "HEAD")
    git(world.root, "checkout", "--quiet", "feat")
    return side


def _empty(world: World, message: str) -> None:
    world.commit({}, message)


def _record_only(world: World, message: str) -> None:
    world.commit({FINDINGS: phase6(world.reviewed) + "\nrecord\n", "plans/INDEX.md": "# Index 2\n"}, message)


def _clean_main_merge(world: World, message: str) -> None:
    _merge(world, world.main_tip, message)


def _code_change(world: World, message: str) -> None:
    world.commit({"src/app.py": "value = 3\n"}, message)


def _docs_change(world: World, message: str) -> None:
    world.commit({"docs/guide.md": "guide\n"}, message)


def _altered_main_merge(world: World, message: str) -> None:
    _merge(world, world.main_tip, message, alter=True)


def _side_branch_merge(world: World, message: str) -> None:
    _merge(world, _side_branch(world), message)


FOLLOWERS: dict[str, tuple[Callable[[World, str], None], bool]] = {
    "empty": (_empty, True),
    "record-only": (_record_only, True),
    "clean-main-merge": (_clean_main_merge, True),
    "code-change": (_code_change, False),
    "docs-change": (_docs_change, False),
    "altered-main-merge": (_altered_main_merge, False),
    "merge-of-a-side-branch": (_side_branch_merge, False),
}


@pytest.mark.parametrize("case", list(FOLLOWERS))
def test_only_allowed_commits_follow_review(
    make: Callable[..., World], capsys: pytest.CaptureFixture[str], case: str
) -> None:
    """Criterion 7. Planted fault: a code change, a foreign merge or an altered merge of main after the reviewed
    commit reaches admission, or a record-only, empty or clean main merge is refused."""
    follow, expected = FOLLOWERS[case]
    world = make(main_ahead=True)
    follow(world, f"after the review\n\n{TRAILER}")
    world.publish()
    if expected:
        admitted(world, capsys)
    else:
        err = refused(world, capsys)
        found = [line for line in refusal_lines(err) if line.startswith("post-review: ")]
        assert found and not any("not evaluated" in line for line in found), err


def test_regenerated_index_in_main_merge(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """A main merge may regenerate the index, but may not invent an index or alter other paths."""
    files = {**DEFAULT_CHANGE}
    for name in ("plans_registry.py", "_verdict.py", "venv_guard.py"):
        files[f"scripts/{name}"] = (REPO / "scripts" / name).read_bytes()
    world = make(main_ahead=True, change=files)
    git(world.root, "merge", "--quiet", "--no-ff", "--no-commit", world.main_tip)
    subprocess.run(
        [sys.executable, str(world.root / "scripts/plans_registry.py"), "--index"],
        cwd=world.root,
        check=True,
        capture_output=True,
    )
    git(world.root, "add", "plans/INDEX.md")
    git(world.root, "commit", "--quiet", "-m", f"sync main\n\n{TRAILER}")
    world.publish()
    admitted(world, capsys)

    git(world.root, "reset", "--hard", "HEAD^")
    git(world.root, "merge", "--quiet", "--no-ff", "--no-commit", world.main_tip)
    write(world.root, {"plans/INDEX.md": "invented index\n"})
    git(world.root, "add", "plans/INDEX.md")
    git(world.root, "commit", "--quiet", "-m", f"sync main\n\n{TRAILER}")
    world.publish()
    world.gh.calls.clear()
    assert "post-review:" in refused(world, capsys)


# ---------------------------------------------------------------------------
# Criteria 8 and 24: required checks
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("states", "expected"),
    [
        ([], "required check `verify` is absent on the head"),
        ([("lint", "SUCCESS")], "required check `verify` is absent on the head"),
        ([("verify", "PENDING")], "required check `verify` is pending on the head"),
        ([("verify", "FAILURE")], "required check `verify` concluded FAILURE on the head"),
        ([("verify", "SUCCESS"), ("verify", "CANCELLED")], "required check `verify` concluded CANCELLED on the head"),
        ([("verify", "SUCCESS")], None),
        ([("verify", "SKIPPED")], None),
        ([("verify", "NEUTRAL")], None),
    ],
    ids=["none", "other-only", "pending", "failure", "one-cancelled", "success", "skipped", "neutral"],
)
def test_ruleset_checks_on_head(
    make: Callable[..., World],
    capsys: pytest.CaptureFixture[str],
    states: list[tuple[str, str]],
    expected: str | None,
) -> None:
    """Criterion 8. Planted fault: a missing, pending or failing required check passes, or SUCCESS, SKIPPED or
    NEUTRAL is rejected; the checks read are those of the verified head."""
    world = make()
    world.gh.states = states
    if expected is None:
        admitted(world, capsys)
    else:
        err = refused(world, capsys)
        assert f"checks: {expected}" in err
    assert ("head_checks", world.head) in world.gh.calls


def test_rollup_states_are_normalized() -> None:
    """The rollup reader behind criterion 8: a run without a conclusion is pending, never passed."""
    nodes = [
        {"__typename": "CheckRun", "name": "a", "status": "IN_PROGRESS", "conclusion": None},
        {"__typename": "CheckRun", "name": "b", "status": "COMPLETED", "conclusion": "SUCCESS"},
        {"__typename": "CheckRun", "name": "c", "status": "COMPLETED", "conclusion": None},
        {"__typename": "StatusContext", "context": "d", "state": "EXPECTED"},
        {"__typename": "StatusContext", "context": "e", "state": "SUCCESS"},
    ]
    assert ep.normalize_rollup(nodes) == [
        ("a", "PENDING"),
        ("b", "SUCCESS"),
        ("c", "NO CONCLUSION"),
        ("d", "PENDING"),
        ("e", "SUCCESS"),
    ]
    for bad in (None, [{"__typename": "Other"}], [{"__typename": "CheckRun", "status": "COMPLETED"}]):
        with pytest.raises(ep.Unreadable):
            ep.normalize_rollup(bad)


def _rules(*contexts: str) -> list[dict]:
    checks = [{"context": context} for context in contexts]
    return [{"type": "required_status_checks", "parameters": {"required_status_checks": checks}}]


def test_required_checks_union(make: Callable[..., World], capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    """Criterion 24. Planted fault: a check required by one ruleset or by classic protection is omitted, or an
    unreadable source allows admission."""
    rules = [*_rules("verify"), {"type": "merge_queue", "parameters": {}}, *_rules("lint")]
    branch = {"protection": {"required_status_checks": {"contexts": ["legacy"], "checks": [{"context": "app"}]}}}
    assert ep.union_required(rules, branch) == {"verify", "lint", "legacy", "app"}
    assert ep.union_required(_rules("verify"), {"protection": {"enabled": False}}) == {"verify"}
    assert ep.union_required(rules, {}) == {"verify", "lint"}
    assert ep.union_required(rules, {"protection": None}) == {"verify", "lint"}
    for bad_rules, bad_branch in (
        (None, branch),
        ([{"parameters": {}}], branch),
        ([{"type": "required_status_checks", "parameters": {}}], branch),
        (_rules(""), branch),
        (rules, {"protection": "invalid"}),
        (rules, {"protection": {"required_status_checks": {"contexts": [None]}}}),
    ):
        with pytest.raises(ep.Unreadable):
            ep.union_required(bad_rules, bad_branch)

    # The adapter reads both sources and unions them; a failed read of either is unreadable.
    repo = (0, json.dumps({"owner": {"login": "o"}, "name": "r"}), "")
    fake = FakeRun(
        [
            repo,
            (0, json.dumps(rules), ""),
            (0, json.dumps({"protected": True}), ""),
            (0, json.dumps(branch["protection"]["required_status_checks"]), ""),
        ]
    )
    assert ep.GitHub(tmp_path, run=fake).required_checks("main") == {"verify", "lint", "legacy", "app"}
    assert fake.argv[1][:2] == ["gh", "api"] and fake.argv[1][2] == "repos/o/r/rules/branches/main?per_page=100"
    assert fake.argv[2] == ["gh", "api", "repos/o/r/branches/main"]
    unprotected = FakeRun([repo, (0, json.dumps(rules), ""), (1, "", "Branch not protected (HTTP 404)")])
    assert ep.GitHub(tmp_path, run=unprotected).required_checks("main") == {"verify", "lint"}
    failing = FakeRun([repo, (0, json.dumps(rules), ""), (1, "", "HTTP 403")])
    with pytest.raises(ep.Unreadable):
        ep.GitHub(tmp_path, run=failing).required_checks("main")

    # The command needs every check of the union on the head.
    world = make()
    world.gh.required = {"verify", "lint"}
    err = refused(world, capsys)
    assert "checks: required check `lint` is absent on the head" in err


# ---------------------------------------------------------------------------
# Criterion 9: decision pull requests
# ---------------------------------------------------------------------------


def test_decision_pr_refused_unattended(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 9. Planted fault: a pull request with the decision label or a path under docs/adr/ is admitted."""
    labelled = make()
    labelled.gh.pr = dataclasses.replace(labelled.gh.pr, labels=("decision",))
    err = refused(labelled, capsys)
    assert "decision: the pull request carries the `decision` label" in err

    adr = make(change={**DEFAULT_CHANGE, "docs/adr/0099-example.md": "# ADR\n"})
    err = refused(adr, capsys)
    assert "decision: the pull request touches docs/adr/ (docs/adr/0099-example.md)" in err

    other = make()
    other.gh.pr = dataclasses.replace(other.gh.pr, labels=("enhancement",))
    admitted(other, capsys)


# ---------------------------------------------------------------------------
# Criterion 10: unreadable evidence
# ---------------------------------------------------------------------------


class FakeRun:
    """A stand-in for `subprocess.run` under the GitHub adapter: answers in order, records each argv."""

    def __init__(self, answers: list[tuple[int, str, str]]) -> None:
        self.answers = list(answers)
        self.argv: list[list[str]] = []

    def __call__(self, argv: list[str], **_options: object) -> subprocess.CompletedProcess:
        self.argv.append(list(argv))
        code, out, err = self.answers.pop(0)
        return subprocess.CompletedProcess(argv, code, out, err)


def _pr_payload(**overrides: object) -> dict:
    node = {
        "id": "PR_node7",
        "number": 7,
        "state": "OPEN",
        "isDraft": False,
        "baseRefName": "main",
        "headRefOid": "a" * 40,
        "isCrossRepository": False,
        "isInMergeQueue": False,
        "labels": {"pageInfo": {"hasNextPage": False}, "nodes": [{"name": "x"}]},
        **overrides,
    }
    return {"data": {"repository": {"pullRequest": node}}}


def test_unreadable_evidence_refused(
    make: Callable[..., World], capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    """Criterion 10. Planted fault: unreadable, ambiguous or missing evidence reaches admission."""
    world = make()
    world.gh.failing = {"pull_request"}
    err = refused(world, capsys)
    assert "pr: the pull request could not be read" in err
    for condition in ep.CONDITIONS[2:]:
        assert f"{condition}: not evaluated: pr" in err

    for failing, line in (
        ("required_checks", "checks: the required checks of main could not be read"),
        ("head_checks", "checks: the checks on the head could not be read"),
    ):
        world = make()
        world.gh.failing = {failing}
        assert line in refused(world, capsys)

    world = make()
    world.gh.required = set()
    assert "checks: no required check is declared for main" in refused(world, capsys)

    world = make()
    world.tracker_error = "the tracker render is not readable"
    assert "trailer: the tracker could not be read" in refused(world, capsys)

    world = make(record=lambda reviewed, _main: {"plans/changes/demo/notes.md": phase6(reviewed)})
    assert "phase-6: plans/changes/demo/findings.md is not readable at the head" in refused(world, capsys)

    world = make(change={**DEFAULT_CHANGE, SPEC: "---\nbead: [unclosed\n---\n"})
    assert "change: a header is not valid YAML" in refused(world, capsys)

    world = make()
    git(world.root, "remote", "set-url", "origin", str(world.root.parent / "missing.git"))
    err = refused(world, capsys)
    assert "script: the script could not be compared" in err
    for condition in ("pr", "head", "change", "trailer", "checks", "decision"):
        assert f"{condition}: not evaluated: script" in err
    assert ("head_checks", world.head) not in world.gh.calls

    # The adapter: a malformed or incomplete answer is unreadable, never a default.
    for payload in (
        {"data": None},
        {"data": {"repository": {"pullRequest": None}}},
        _pr_payload(isDraft="no"),
        _pr_payload(number=8),
        _pr_payload(headRefOid="abc"),
        _pr_payload(labels={"pageInfo": {"hasNextPage": True}, "nodes": []}),
    ):
        with pytest.raises(ep.Unreadable):
            ep.parse_pull_request(payload, 7)
    assert ep.parse_pull_request(_pr_payload(), 7).labels == ("x",)
    repo = (0, json.dumps({"owner": {"login": "o"}, "name": "r"}), "")
    for answer in ((1, "", "HTTP 502"), (0, "not json", ""), (0, json.dumps({"errors": [{"message": "no"}]}), "")):
        with pytest.raises(ep.Unreadable):
            ep.GitHub(tmp_path, run=FakeRun([repo, answer])).pull_request(7)


# ---------------------------------------------------------------------------
# Criteria 11, 12, 14, 15 and 17: the mutation and its results
# ---------------------------------------------------------------------------


def test_pinned_enqueue_mutation(
    make: Callable[..., World], capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    """Criterion 11. Planted fault: the mutation carries another or no head, or the command can merge directly."""
    world = make()
    pull_ref = git(world.origin, "rev-parse", "refs/pull/7/head")
    admitted(world, capsys)
    assert world.gh.enqueued() == [("PR_node7", pull_ref)]

    # GitHub reporting a head the pull ref does not hold is no verified head.
    stale = make()
    stale.gh.pr = dataclasses.replace(stale.gh.pr, head_oid=stale.reviewed)
    err = refused(stale, capsys)
    assert f"head: GitHub reports head {stale.reviewed}, origin's pull ref holds {stale.head}" in err

    head = "c" * 40
    answer = {"data": {"enqueuePullRequest": {"mergeQueueEntry": {"position": 2, "state": "QUEUED"}}}}
    fake = FakeRun([(0, json.dumps(answer), "")])
    assert ep.GitHub(tmp_path, run=fake).enqueue("PR_x", head) == {"position": 2, "state": "QUEUED"}
    expected_argv = ["gh", "api", "graphql", "-f", f"query={ep.ENQUEUE_MUTATION}", "-f", "pullRequestId=PR_x"]
    assert fake.argv == [[*expected_argv, "-f", f"expectedHeadOid={head}"]]
    pinned = "enqueuePullRequest(input: {pullRequestId: $pullRequestId, expectedHeadOid: $expectedHeadOid})"
    assert pinned in ep.ENQUEUE_MUTATION
    with pytest.raises(ep.AdmissionError):
        ep.GitHub(tmp_path, run=FakeRun([(1, "", "GraphQL: rejected")])).enqueue("PR_x", head)

    source = Path(ep.__file__).read_text(encoding="utf-8")
    for forbidden in ("mergePullRequest", "enablePullRequestAutoMerge", "--admin", "pr merge", "/merge"):
        assert forbidden not in source, f"the admission command names {forbidden!r}"
    assert source.count("mutation(") == 1, "the admission command holds a second mutation"


def test_moved_head_is_not_retried(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 12. Planted fault: a moved head is retried, or the report omits either head."""
    world = make()
    moved = "b" * 40
    world.gh.enqueue_error = "GraphQL: Head sha didn't match expected head sha"
    world.gh.head_after_error = moved
    assert world.run("7") == 1
    err = capsys.readouterr().err
    assert f"head-moved: expected head {world.head}, GitHub reports {moved}; not retried." in err
    assert world.gh.enqueued() == [("PR_node7", world.head)], "the moved head was retried"


def test_admitted_result(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 14. Planted fault: success reports merged or exits nonzero."""
    world = make()
    out = admitted(world, capsys)
    assert "queued" in out
    assert "merged" not in out.lower(), "queue admission was reported as a merge"
    assert world.gh.names().count("enqueue") == 1


def test_already_queued_is_idempotent(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 15. Planted fault: a queued request is enqueued again, evaluated, or reported as an error."""
    world = make()
    # Every other condition would refuse: the queued state ends the run before any is evaluated.
    world.gh.pr = dataclasses.replace(world.gh.pr, in_merge_queue=True, is_draft=True, labels=("decision",))
    world.gh.failing = {"required_checks", "head_checks"}
    for _ in range(2):
        assert world.run("7") == 0
        captured = capsys.readouterr()
        assert captured.out.startswith("already queued: PR #7")
        assert captured.err == ""
    assert world.gh.names() == ["pull_request", "pull_request"]

    world.script.write_text("# modified\n", encoding="utf-8")
    world.gh.calls.clear()
    err = refused(world, capsys)
    assert "script: " in err
    assert world.gh.calls == [], "script integrity must be checked before reading a queued request"


def test_refusals_report_all_identifiers(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 16. Planted fault: a determinable failure is omitted, has no identifier, or exits 0."""
    world = make(
        change={"src/app.py": "value = 2\n"},
        record=lambda reviewed, _main: {"plans/notes/findings.md": phase6(reviewed)},
    )
    world.gh.pr = dataclasses.replace(world.gh.pr, is_draft=True, labels=("decision",))
    world.gh.states = [("verify", "FAILURE")]
    err = refused(world, capsys)
    lines = refusal_lines(err)
    assert lines == [
        "pr: the pull request is a draft",
        "change: the diff touches 0 change folders; exactly one is required",
        "phase-6: not evaluated: change",
        "reviewed-commit: not evaluated: phase-6",
        "post-review: not evaluated: reviewed-commit",
        "checks: required check `verify` concluded FAILURE on the head",
        "decision: the pull request carries the `decision` label; it is the maintainer's",
    ]


def test_usage_and_mutation_failures(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 17. Planted fault: a usage error or a failed admission exits 0 or 1."""
    world = make()
    for argv in ([], ["abc"], ["0"], ["-3"], ["7", "8"], ["7", "--bogus"], ["7", "--admin"]):
        assert world.run(*argv) == 2, argv
        assert capsys.readouterr().err.startswith("usage: ")
    assert world.gh.calls == [], "an invalid invocation reached GitHub"

    world.gh.enqueue_error = "GraphQL: the merge queue is not enabled"
    assert world.run("7") == 2
    assert "admission-failed: PR #7" in capsys.readouterr().err
    assert world.gh.names().count("enqueue") == 1

    unread = make()
    unread.gh.enqueue_error = "GraphQL: something failed"
    unread.gh.reread_fails = True
    assert unread.run("7") == 2
    assert "admission-failed: PR #7" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Criterion 18: the script's own blob
# ---------------------------------------------------------------------------


def test_modified_script_refuses(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """Criterion 18. Planted fault: the checker admits while its blob differs from origin's main."""
    world = make()
    world.script.write_bytes(REAL_SCRIPT + b"# an edit\n")
    err = refused(world, capsys)
    assert any(line.startswith("script: this checkout's scripts/enqueue_pr.py") for line in refusal_lines(err))

    other = make(script_on_main=False)
    err = refused(other, capsys)
    assert any(line.startswith("script: ") for line in refusal_lines(err))

    unchanged = make()
    admitted(unchanged, capsys)


# ---------------------------------------------------------------------------
# Criterion 21: maintainer mode
# ---------------------------------------------------------------------------


def _draft(world: World) -> None:
    world.gh.pr = dataclasses.replace(world.gh.pr, is_draft=True)


def _failing_check(world: World) -> None:
    world.gh.states = [("verify", "FAILURE")]


def _stale_head(world: World) -> None:
    world.gh.pr = dataclasses.replace(world.gh.pr, head_oid=world.reviewed)


def _edited_script(world: World) -> None:
    world.script.write_bytes(REAL_SCRIPT + b"# an edit\n")


RETAINED: list[tuple[str, Callable[[World], None]]] = [
    ("pr", _draft),
    ("checks", _failing_check),
    ("head", _stale_head),
    ("script", _edited_script),
]


def test_maintainer_mode_bypasses_only_specified_conditions(
    make: Callable[..., World], capsys: pytest.CaptureFixture[str]
) -> None:
    """Criterion 21. Planted fault: maintainer mode requires a skipped condition, or admits an ineligible request,
    a failing check, an unverified head or a modified script."""
    broken = {
        "trailers": (),
        "change": {**DEFAULT_CHANGE, "docs/adr/0099-example.md": "# ADR\n"},
        "record": lambda _reviewed, _main: {FINDINGS: phase6(None, body=table("open"))},
    }
    world = make(**broken)
    world.gh.pr = dataclasses.replace(world.gh.pr, labels=("decision",))
    refused(world, capsys)
    out = admitted(world, capsys, "--maintainer")
    assert "maintainer mode: skipped change, trailer, phase-6, reviewed-commit, post-review, decision" in out

    for condition, plant in RETAINED:
        world = make(**broken)
        plant(world)
        err = refused(world, capsys, "--maintainer")
        assert any(line.startswith(f"{condition}: ") for line in refusal_lines(err)), condition


def test_human_decided_paths_make_a_decision_pr(make: Callable[..., World], capsys: pytest.CaptureFixture[str]) -> None:
    """Loop row L2-8 (decision S-25): a path provenance.yaml reserves for human-decided is a decision PR."""
    world = make(change={**DEFAULT_CHANGE, "decisions/gates.yaml": "gates: []\n"})
    git(world.root, "checkout", "--quiet", "-b", "mapping", world.base)
    world.commit(
        {"provenance.yaml": 'paths:\n  - prefix: "decisions/gates.yaml"\n    allowed: [human-decided]\n'}, "map"
    )
    git(world.root, "push", "--quiet", "origin", "HEAD:refs/heads/main")
    git(world.root, "checkout", "--quiet", "feat")
    err = refused(world, capsys)
    assert "decision: the pull request touches paths provenance.yaml reserves for human-decided" in err
    assert "decisions/gates.yaml" in err


@pytest.mark.parametrize("spelling", ["--maint", "--main", "--m"])
def test_maintainer_mode_needs_the_full_option(spelling: str) -> None:
    """Loop row L2-2: an abbreviated --maintainer is a usage error, never maintainer mode."""
    with pytest.raises(ep.UsageError):
        ep.parse_args(["54", spelling])


@pytest.mark.parametrize(
    "argv",
    [
        ["--maintainer", "7"],
        ["--maintainer"],
        ["--", "7", "--maintainer"],
        ["--", "7"],
        ["7", "--maintainer", "--maintainer"],
    ],
)
def test_maintainer_flag_before_number_is_refused(
    make: Callable[..., World], capsys: pytest.CaptureFixture[str], argv: list[str]
) -> None:
    """Phase-6 F-1: `--maintainer` or any flag before `<number>` is refused with exit 2 so no accepted
    spelling can bypass the `* --maintainer*` permission rule."""
    world = make()
    assert world.run(*argv) == 2, argv
    assert capsys.readouterr().err.startswith("usage: ")
    assert world.gh.calls == [], "an invalid flag order reached GitHub"


def test_decision_map_uses_main_and_longest_prefix(make, capsys):
    """Loop rows L3-5 and L4-1. Planted fault: reading the working tree or a stale local origin/main ref instead
    of the fetched main commit, or ignoring longest-prefix overrides in provenance.yaml."""
    world = make(change={**DEFAULT_CHANGE, "docs/governance/fehler-katalog.md": "change"})
    mapping = "paths:\n  - prefix: docs/governance/\n    allowed: [human-decided]\n  - prefix: docs/governance/fehler-katalog.md\n    allowed: [ai-drafted-reviewed]\n  - prefix: docs/mixed/\n    allowed: [human-decided, ai-drafted-reviewed]\n"
    git(world.root, "checkout", "--quiet", "-b", "mapping", world.base)
    world.commit({"provenance.yaml": mapping}, "map")
    git(world.root, "push", "--quiet", "origin", "HEAD:refs/heads/main")
    git(world.root, "checkout", "--quiet", "feat")
    write(world.root, {"provenance.yaml": "paths: []\n"})
    admitted(world, capsys)
    reserved = make(change={**DEFAULT_CHANGE, "docs/governance/quality.md": "change"})
    stale_base = reserved.base
    git(reserved.root, "checkout", "--quiet", "-b", "mapping", reserved.base)
    reserved.commit({"provenance.yaml": mapping}, "map")
    git(reserved.root, "push", "--quiet", "origin", "HEAD:refs/heads/main")
    # Force local origin/main back to the stale base commit to prove the fetched main commit is read (L4-1).
    git(reserved.root, "update-ref", "refs/remotes/origin/main", stale_base)
    git(reserved.root, "checkout", "--quiet", "feat")
    write(reserved.root, {"provenance.yaml": "paths: []\n"})
    assert "decision:" in refused(reserved, capsys)
    assert not ep.is_human_decided("docs/mixed/file.md", ep.human_decided_prefixes(world.root))


def test_malformed_provenance_refuses(make, capsys):
    """Loop row L3-6. Planted fault: letting invalid YAML in provenance.yaml raise an unhandled exception
    instead of refusing under the decision condition."""
    world = make()
    git(world.root, "checkout", "--quiet", "-b", "mapping", world.base)
    world.commit({"provenance.yaml": "paths: [broken\n"}, "bad map")
    git(world.root, "push", "--quiet", "origin", "HEAD:refs/heads/main")
    git(world.root, "checkout", "--quiet", "feat")
    try:
        result = world.run("7")
    except yaml.YAMLError as error:
        pytest.fail(f"malformed provenance must refuse without an exception: {error}")
    assert result == 1
    assert "decision:" in capsys.readouterr().err


def test_malformed_released_row_refuses():
    """Loop row L3-7. Planted fault: silently skipping malformed or unescaped-pipe lines in a released loop block."""
    for row in (
        "| L1-1 | MAJOR | CODE | x | y | bad | pipe | m | open | — | — |",
        "| wrong | MAJOR | CODE | x | y | finding | m | open | — | — |",
    ):
        text = "## Phase 4b — loop rows, released\n" + RELEASED_HEADER + "\n" + row
        assert any("unrecognised" in problem for problem in ep.released_problems(text))


def test_merge_check_uses_shared_engine(monkeypatch, tmp_path):
    """Loop row L3-8. Planted fault: re-implementing git merge-tree parsing instead of calling pr_sync.merge_tree."""
    calls = []
    monkeypatch.setattr(ep, "_is_ancestor", lambda *_args: True)
    monkeypatch.setattr(pr_sync, "merge_tree", lambda *args: (calls.append(args) or ("a" * 40, [])))
    monkeypatch.setattr(ep, "_git", lambda *_args: "a" * 40)
    try:
        problems = ep.commit_problems(tmp_path, "b" * 40, ["c" * 40, "d" * 40], "demo", "main")
    except ep.Unreadable as error:
        pytest.fail(f"the shared merge engine must be used: {error}")
    assert problems == []
    assert calls


def test_unicode_reviewer_no_finding():
    """Loop row L3-9. Planted fault: rejecting a non-ASCII reviewer name on a no-finding verdict line."""
    block = ["## Phase 6", "Émile reported no finding.", VERDICT]
    assert ep.phase6_problems(block) == []


def test_failed_enqueue_rereads_queue_state(make, capsys):
    """Loop row L3-10. Planted fault: reporting not-queued after a transport error when GitHub accepted the mutation."""
    world = make()
    world.gh.enqueue_error = "connection lost"
    original = world.gh.pull_request

    def reread(number):
        pr = original(number)
        return dataclasses.replace(pr, in_merge_queue=True) if world.gh.enqueued() else pr

    world.gh.pull_request = reread
    assert world.run("7") == 0
    assert "already queued" in capsys.readouterr().out


def test_required_check_respects_ruleset_app_identity() -> None:
    rules = [
        {
            "type": "required_status_checks",
            "parameters": {
                "required_status_checks": [
                    {"context": "verify", "integration_id": 42},
                ]
            },
        }
    ]
    required = ep.union_required(rules, {})
    assert required == {("verify", 42)}
    nodes = [
        {
            "__typename": "CheckRun",
            "name": "verify",
            "status": "COMPLETED",
            "conclusion": "SUCCESS",
            "checkSuite": {"app": {"databaseId": 99}},
        }
    ]
    states = ep.normalize_rollup(nodes)
    github = type(
        "Checks", (), {"required_checks": lambda _self, _branch: required, "head_checks": lambda _self, _head: states}
    )()
    assert ep.checks_problems(github, "head")
    nodes[0]["checkSuite"]["app"]["databaseId"] = 42
    states = ep.normalize_rollup(nodes)
    assert not ep.checks_problems(github, "head")
    assert "checkSuite" in ep.ROLLUP_QUERY and "databaseId" in ep.ROLLUP_QUERY


def test_post_review_spec_and_code_are_not_records(make: Callable[..., World]) -> None:
    world = make()
    for path in (SPEC, "plans/changes/demo/tool.py"):
        head = world.commit({path: "substantive change\n"}, "unreviewed change")
        assert ep.post_review_problems(world.root, world.reviewed, head, "demo", world.main_tip)


def test_classic_required_check_uses_app_identity(tmp_path: Path) -> None:
    repo = (0, json.dumps({"owner": {"login": "o"}, "name": "r"}), "")
    branch = (0, json.dumps({"protected": True}), "")
    checks = (0, json.dumps({"contexts": ["verify"], "checks": [{"context": "verify", "app_id": 42}]}), "")
    fake = FakeRun([repo, (0, "[]", ""), branch, checks])
    required = ep.GitHub(tmp_path, run=fake).required_checks("main")
    assert ("verify", 42) in required
    assert fake.argv[3] == ["gh", "api", "repos/o/r/branches/main/protection/required_status_checks"]
    assert ep.checks_problems(
        type(
            "GH",
            (),
            {"required_checks": lambda _self, _: required, "head_checks": lambda _self, _: [("verify", "SUCCESS", 99)]},
        )(),
        "a",
    )


def test_classic_duplicate_context_respects_required_app() -> None:
    classic = {
        "protection": {
            "required_status_checks": {
                "contexts": ["verify", "legacy"],
                "checks": [{"context": "verify", "app_id": 42}],
            }
        }
    }
    required = ep.union_required([], classic)
    github = type(
        "GH",
        (),
        {
            "required_checks": lambda _self, _branch: required,
            "head_checks": lambda _self, _head: [
                ("verify", "SUCCESS", 42),
                ("verify", "FAILURE", 99),
                ("legacy", "SUCCESS"),
            ],
        },
    )()
    assert not ep.checks_problems(github, "head")
    assert ("verify", 42) in required and "verify" not in required


# ---------------------------------------------------------------------------
# enqueue-pr-rulesets: ruleset-only protection and the runner's state line
# ---------------------------------------------------------------------------

RULESET_ONLY_404 = "gh: Branch not protected (HTTP 404)"


def _ruleset_only_github(tmp_path: Path, classic: tuple[int, str, str]) -> ep.GitHub:
    """The adapter over a branch that reports protected, with `classic` as the required-checks answer."""
    repo = (0, json.dumps({"owner": {"login": "o"}, "name": "r"}), "")
    rules = (0, json.dumps([*_rules("verify"), {"type": "merge_queue", "parameters": {}}, *_rules("lint")]), "")
    branch = (0, json.dumps({"protected": True}), "")
    return ep.GitHub(tmp_path, run=FakeRun([repo, rules, branch, classic]))


def test_ruleset_only_branch_without_classic_protection(tmp_path: Path) -> None:
    """Criterion 1. Planted fault: the classic endpoint's `Branch not protected` 404 on a branch that reports
    protected is refused, or a ruleset check disappears from the required set."""
    github = _ruleset_only_github(tmp_path, (1, "", RULESET_ONLY_404))
    try:
        required = github.required_checks("main")
    except ep.Unreadable as error:
        pytest.fail(f"a ruleset-only branch must yield the ruleset checks: {error}")
    assert required == {"verify", "lint"}


@pytest.mark.parametrize(
    ("states", "expected"),
    [
        ([("verify", "SUCCESS")], "required check `lint` is absent on the head"),
        ([("verify", "SUCCESS"), ("lint", "FAILURE")], "required check `lint` concluded FAILURE on the head"),
        ([("verify", "SUCCESS"), ("lint", ep.PENDING)], "required check `lint` is pending on the head"),
    ],
    ids=["missing", "failing", "pending"],
)
def test_ruleset_only_branch_requires_head_checks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, states: list[tuple[str, str]], expected: str
) -> None:
    """Criterion 2. Planted fault: on a ruleset-only branch a missing or unsuccessful ruleset check passes."""
    github = _ruleset_only_github(tmp_path, (1, "", RULESET_ONLY_404))
    monkeypatch.setattr(github, "head_checks", lambda _head: states)
    problems = ep.checks_problems(github, "a" * 40)
    assert expected in problems
    passing = _ruleset_only_github(tmp_path, (1, "", RULESET_ONLY_404))
    monkeypatch.setattr(passing, "head_checks", lambda _head: [("verify", "SUCCESS"), ("lint", "SUCCESS")])
    assert ep.checks_problems(passing, "a" * 40) == []


@pytest.mark.parametrize(
    "diagnostic",
    ["gh: Not Found (HTTP 404)", "gh: Resource not accessible by integration (HTTP 403)", "Branch not protected"],
    ids=["unrelated-404", "403", "no-404"],
)
def test_classic_protection_other_errors_refuse(tmp_path: Path, diagnostic: str) -> None:
    """Criterion 3. Planted fault: an unrelated 404, a 403 or a message without the 404 at the classic
    required-checks endpoint is taken as absent protection."""
    with pytest.raises(ep.Unreadable):
        _ruleset_only_github(tmp_path, (1, "", diagnostic)).required_checks("main")
    problems = ep.checks_problems(_ruleset_only_github(tmp_path, (1, "", diagnostic)), "a" * 40)
    assert len(problems) == 1 and "could not be read" in problems[0]


def _released_with(line: str) -> str:
    return released((FIXED, "agree")).replace("\n\nRounds run: 1", f"\n\n{line}\n\nRounds run: 1")


@pytest.mark.parametrize(
    "line",
    [
        'Loop state: {"round": 2, "note": "a | b"}',
        'Loop state: {"members": ["x|y"], "next": "review"} \t',
        'Loop state: {"round": 1}',
    ],
    ids=["pipe", "pipe-trailing-space", "no-pipe"],
)
def test_released_runner_state_line_is_accepted(line: str) -> None:
    """Criterion 4. Planted fault: the runner's `Loop state: {…}` line with a pipe in its state is refused as an
    unrecognised table line in a released block."""
    import stage2  # the copy of the prefix must not drift from the runner's own

    assert stage2.STATE_KEY == ep.LOOP_STATE_PREFIX
    assert ep.released_problems(_released_with(line)) == []


@pytest.mark.parametrize(
    "line",
    [
        "Loop state: {not json | x}",
        'Loop state: ["a | b"]',
        'Loop state: "a | b"',
        'loop state: {"a": "b | c"}',
        'Loop state:{"a": "b | c"}',
        'Loop state: {"a": "b | c"} trailing',
        ' Loop state: {"a": "b | c"}',
        "an unrelated line | with a pipe",
    ],
    ids=["not-json", "array", "string", "case", "no-space", "trailing-text", "indented", "unrelated"],
)
def test_released_state_lookalikes_refuse(line: str) -> None:
    """Criterion 5. Planted fault: a pipe-bearing line that is not the runner's state line passes in a released
    block, or a pipe-bearing `Loop state:` line passes in a `## Phase 6` block."""
    problems = ep.released_problems(_released_with(line))
    assert any("unrecognised table line in the released block" in problem for problem in problems), problems
    runner_line = 'Loop state: {"round": 2, "note": "a | b"}'
    phase6_block = ep.last_phase6_block(phase6("a" * 40, body=f"{NO_FINDING}\n\n{runner_line}"))
    assert phase6_block is not None
    assert any("unrecognised table line" in problem for problem in ep.phase6_problems(phase6_block))


def test_released_state_extra_whitespace_is_accepted() -> None:
    """JSON whitespace after the exact prefix does not invalidate an object."""
    for whitespace in (" ", "\t"):
        line = f'Loop state: {whitespace}{{"a": "b | c"}}'
        assert ep.released_problems(_released_with(line)) == []
