"""Tests for scripts/archive_closed_changes.py (bead coding-harness-cqun).

Every test runs against a temporary fixture repository with its own tracker
render — never against this checkout's real plans/ tree or its tracker. The
real registry generator, the real criterion-ledger checker and the real
Makefile are reused, so the tests hold the tool to the contracts it must
satisfy: the plans-registry coupling, the generated index format, the
criterion-ledger gate, and close-merged's argument discipline.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import archive_closed_changes as archive  # noqa: E402 — the module under test
import bead_render  # noqa: E402 — the patched tracker access point
import check_criterion_ledger  # noqa: E402 — the real ledger gate, reused
import plans_registry as reg  # noqa: E402 — the real generator and checker, reused

# The controlled archiving day every write run of this module uses.
DAY = dt.date(2026, 3, 4)


# ---------------------------------------------------------------------------
# The fixture repository
# ---------------------------------------------------------------------------


def _artefact(
    title: str,
    bead: str | None,
    *,
    status: str = "draft",
    implementation: str = "none",
    date: str = "2026-10-01",
    reviewed: str = "2026-10-02",
    updated: str | None = "2026-10-02",
    body: str = "Artefact body that must survive the move unchanged.\n",
) -> str:
    """One change artefact with a realistic, valid front-matter header."""
    header = [
        "---",
        f'title: "{title}"',
        f"status: {status}",
        f"implementation_status: {implementation}",
        f"date: {date}",
        f"last_reviewed: {reviewed}",
    ]
    if bead is not None:
        header.append(f"bead: {bead}")
    if updated is not None:
        header.append(f"updated: {updated}")
    header += [
        "supersedes: null",
        "superseded_by: null",
        'produced_by: {kind: llm-session, name: fixture, version: "test"}',
        "tags: [fixture]",
    ]
    return "\n".join([*header, "---", "", body])


def _closed_files(bead: str) -> dict[str, str]:
    """The artefact set of an ordinary, complete change folder."""
    return {
        "spec.md": _artefact("Spec — done thing", bead),
        "plan.md": _artefact("Plan — done thing", bead),
        "research.md": _artefact("Research — done thing", bead),
    }


def _archived_files(bead: str) -> dict[str, str]:
    """The artefact set of an already-archived folder (accepted and done)."""
    return {
        "spec.md": _artefact("Spec — old thing", bead, status="accepted", implementation="done"),
        "plan.md": _artefact("Plan — old thing", bead, status="accepted", implementation="done"),
    }


class Fixture:
    """A plans/ tree with its own tracker render and transitional export."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.changes = root / "plans" / "changes"
        self.archive = self.changes / "archive"
        self.render_path = root / "tracker-render.jsonl"
        self.archive.mkdir(parents=True)
        self.render_path.write_text("", encoding="utf-8")

    def add(
        self,
        name: str,
        *,
        files: dict[str, str] | None = None,
        companions: dict[str, bytes] | None = None,
        empty_dirs: list[str] | None = None,
    ) -> Path:
        """One change folder (the name may reach into archive/)."""
        folder = self.changes / name
        folder.mkdir(parents=True)
        for rel, text in (files or {}).items():
            target = folder / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        for rel, payload in (companions or {}).items():
            target = folder / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        for rel in empty_dirs or []:
            (folder / rel).mkdir(parents=True, exist_ok=True)
        return folder

    def set_render(self, rows: dict[str, str]) -> None:
        """One render, two readers: the access point and the fixture export."""
        text = "".join(json.dumps({"id": bead_id, "status": status}) + "\n" for bead_id, status in rows.items())
        self.render_path.write_text(text, encoding="utf-8")
        export = self.root / ".beads" / "issues.jsonl"
        export.parent.mkdir(parents=True, exist_ok=True)
        export.write_text(text, encoding="utf-8")


@pytest.fixture
def plans_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Fixture:
    """A fixture repository; every module constant the tool reads is bent to it."""
    fx = Fixture(tmp_path / "repo")
    monkeypatch.setattr(archive, "REPO", fx.root)
    monkeypatch.setattr(archive, "CHANGES", fx.changes)
    monkeypatch.setattr(archive, "ARCHIVE", fx.archive)
    monkeypatch.setattr(reg, "REPO", fx.root)
    monkeypatch.setattr(reg, "PLANS", fx.root / "plans")
    monkeypatch.setattr(reg, "INDEX", fx.root / "plans" / "INDEX.md")
    monkeypatch.setattr(bead_render, "render_pfad", lambda: fx.render_path)
    monkeypatch.setattr(archive, "_today", lambda: DAY)
    return fx


def _snapshot(root: Path) -> dict[str, bytes]:
    """Every file's bytes by repository-relative path — the mutation probe."""
    return {
        str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file() and not p.is_symlink()
    }


def _meta(text: str) -> tuple[dict, str, str]:
    """(parsed mapping, header block, tail from the closing fence) of one artefact."""
    end = text.find("\n---", 4)
    header = text[4:end]
    return yaml.safe_load(header), header, text[end:]


# ---------------------------------------------------------------------------
# Criterion 1 — the report selects exactly the closed single-bead folders
# ---------------------------------------------------------------------------


def test_only_closed_single_bead_folders_are_selected(plans_repo: Fixture, capsys: pytest.CaptureFixture[str]) -> None:
    fx = plans_repo
    fx.add("closed-one", files=_closed_files("b-closed"))
    fx.add("open-two", files=_closed_files("b-open"))
    fx.add("running-three", files=_closed_files("b-running"))
    fx.add("unknown-four", files=_closed_files("b-unknown"))
    fx.add("mixed-five", files={"spec.md": _artefact("Spec a", "b-first"), "plan.md": _artefact("Plan b", "b-second")})
    fx.add("beadless-six", files={"spec.md": _artefact("Beadless spec", None)})
    fx.add("empty-seven")
    fx.add("archive/2026-01-01-older", files=_archived_files("b-closed"))
    living = fx.root / "plans" / "specs" / "living-capability"
    living.mkdir(parents=True)
    (living / "spec.md").write_text(
        _artefact("Living spec", "b-closed", status="accepted", implementation="done"),
        encoding="utf-8",
    )
    fx.set_render({"b-closed": "closed", "b-open": "open", "b-running": "in_progress"})
    # b-unknown is deliberately absent from the render.

    before = _snapshot(fx.root)
    assert archive.main([]) == 0
    out = capsys.readouterr().out

    assert "would archive plans/changes/closed-one (bead b-closed, closed)" in out
    assert out.count("would archive") == 1, "exactly one folder is eligible"
    assert "-> plans/changes/archive/2026-03-04-closed-one/spec.md" in out
    assert "skipped plans/changes/open-two: bead b-open is open (status: open)" in out
    assert "skipped plans/changes/running-three: bead b-running is open (status: in_progress)" in out
    assert "skipped plans/changes/unknown-four: bead b-unknown does not appear in the tracker render" in out
    assert "skipped plans/changes/mixed-five: artefacts name different beads: b-first, b-second" in out
    assert "skipped plans/changes/beadless-six: no artefact names a bead" in out
    assert "skipped plans/changes/empty-seven: no registry artefacts (nothing to classify)" in out
    assert "nothing written" in out
    # The archive and the living spec are never active candidates.
    assert "2026-01-01-older" not in out
    assert "living-capability" not in out
    assert _snapshot(fx.root) == before, "a report changes no file"


# ---------------------------------------------------------------------------
# Criterion 2 — reporting is read-only through the CLI and through make
# ---------------------------------------------------------------------------


def test_default_cli_and_make_are_read_only(
    plans_repo: Fixture,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fx = plans_repo
    fx.add("closed-one", files=_closed_files("b-closed"), companions={"notes.txt": b"keep"})
    fx.set_render({"b-closed": "closed"})

    def _no_subprocess(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("a report must not start a subprocess")

    sp_names = ("run", "call", "check_call", "check_output", "Popen")
    real = {name: getattr(subprocess, name) for name in sp_names}
    for name in sp_names:
        monkeypatch.setattr(subprocess, name, _no_subprocess)
    before = _snapshot(fx.root)
    assert archive.main([]) == 0
    assert "would archive plans/changes/closed-one" in capsys.readouterr().out
    assert _snapshot(fx.root) == before, "reporting changed a repository file"
    # The make half below genuinely invokes make; the spies guard the CLI only.
    for name in sp_names:
        monkeypatch.setattr(subprocess, name, real[name])

    # The make path: a recording fake stands in for python3, so the real
    # recipe's argv lands in a log instead of this checkout.
    shim = tmp_path / "shim"
    shim.mkdir()
    log = tmp_path / "calls.log"
    log.write_text("", encoding="utf-8")
    fake = shim / "python3"
    fake.write_text(
        '#!/bin/sh\nprintf "cwd %s\\nargv %s\\n" "$PWD" "$*" >> "$ARCHIVE_RECORD"\n',
        encoding="utf-8",
    )
    fake.chmod(0o755)
    env = dict(os.environ)
    env.pop("ARGS", None)
    env["PATH"] = f"{shim}{os.pathsep}{env.get('PATH', '')}"
    env["ARCHIVE_RECORD"] = str(log)
    makefile = REPO_ROOT / "Makefile"

    def _make(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["make", "-f", str(makefile), "archive", *args],
            cwd=tmp_path,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    assert _make().returncode == 0
    assert log.read_text(encoding="utf-8").splitlines() == [
        f"cwd {REPO_ROOT}",
        "argv scripts/archive_closed_changes.py",
    ]
    log.write_text("", encoding="utf-8")

    assert _make("ARGS=--write").returncode == 0
    assert log.read_text(encoding="utf-8").splitlines() == [
        f"cwd {REPO_ROOT}",
        "argv scripts/archive_closed_changes.py --write",
    ]
    log.write_text("", encoding="utf-8")

    # An environment variable cannot silently opt into writing.
    env_args = dict(env)
    env_args["ARGS"] = "--write"
    erg = subprocess.run(
        ["make", "-f", str(makefile), "archive"],
        cwd=tmp_path,
        env=env_args,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert erg.returncode == 0
    assert log.read_text(encoding="utf-8").splitlines() == [
        f"cwd {REPO_ROOT}",
        "argv scripts/archive_closed_changes.py",
    ]
    log.write_text("", encoding="utf-8")

    marker = tmp_path / "expanded"
    for raw in (f"$(shell touch {marker})--write", "--write\n", "--\twrite", "--write "):
        erg = _make(f"ARGS={raw}")
        assert erg.returncode != 0, (raw, erg.stdout, erg.stderr)
        assert "ARGS must be empty or --write" in erg.stderr
        assert not marker.exists(), "make expanded an argument as code"
    assert log.read_text(encoding="utf-8") == "", "a refused invocation never reached the fake"

    extra = tmp_path / "extra.mk"
    extra.write_text("# extra make input\n", encoding="utf-8")
    erg = subprocess.run(
        ["make", "-f", str(makefile), "-f", str(extra), "archive"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert erg.returncode != 0
    assert "exactly one Makefile path" in erg.stderr
    assert log.read_text(encoding="utf-8") == ""


# ---------------------------------------------------------------------------
# Criterion 3 — the write relocates the complete folder on the captured day
# ---------------------------------------------------------------------------


def test_write_moves_complete_folder_on_captured_day(plans_repo: Fixture, capsys: pytest.CaptureFixture[str]) -> None:
    fx = plans_repo
    fx.add(
        "done-one",
        files=_closed_files("b-done") | {"deep/nested.md": _artefact("Nested artefact", "b-done")},
        companions={"notes.txt": b"companion bytes \x00 stay", "assets/logo.bin": bytes(range(64))},
        empty_dirs=["really-empty"],
    )
    fx.set_render({"b-done": "closed"})

    assert archive.main(["--write"]) == 0
    out = capsys.readouterr().out
    target = fx.archive / "2026-03-04-done-one"

    assert not (fx.changes / "done-one").exists(), "the eligible source remains active"
    assert target.is_dir()
    assert (target / "really-empty").is_dir(), "an empty folder travels too"
    assert (target / "notes.txt").read_bytes() == b"companion bytes \x00 stay"
    assert (target / "assets/logo.bin").read_bytes() == bytes(range(64))
    assert (target / "deep/nested.md").is_file()
    assert "plans/changes/done-one/notes.txt -> plans/changes/archive/2026-03-04-done-one/notes.txt (companion)" in out
    assert "plans/changes/done-one/deep/nested.md -> plans/changes/archive/2026-03-04-done-one/deep/nested.md" in out
    assert "archived plans/changes/done-one" in out


# ---------------------------------------------------------------------------
# Criterion 4 — only the four lifecycle header fields change
# ---------------------------------------------------------------------------


def test_only_lifecycle_header_fields_change(plans_repo: Fixture) -> None:
    fx = plans_repo
    original = _artefact("Spec — full", "b-full", date="2026-09-09")
    no_updated = _artefact("Spec — no updated", "b-noup", updated=None)
    fx.add("full-one", files={"spec.md": original, "plan.md": _artefact("Plan — full", "b-full")})
    fx.add("no-updated", files={"spec.md": no_updated})
    fx.set_render({"b-full": "closed", "b-noup": "closed"})

    assert archive.main(["--write"]) == 0

    moved = (fx.archive / "2026-03-04-full-one" / "spec.md").read_text(encoding="utf-8")
    old_meta, old_header, old_tail = _meta(original)
    new_meta, _, new_tail = _meta(moved)
    assert new_tail == old_tail, "the body changed"
    assert new_meta["status"] == "accepted"
    assert new_meta["implementation_status"] == "done"
    assert new_meta["updated"] == DAY
    assert new_meta["last_reviewed"] == DAY
    for key, value in old_meta.items():
        if key not in {"status", "implementation_status", "updated", "last_reviewed"}:
            assert new_meta[key] == value, f"unrelated field {key} changed"

    new_header = _meta(moved)[1]
    old_lines, new_lines = old_header.split("\n"), new_header.split("\n")
    assert len(old_lines) == len(new_lines), "a line was inserted or dropped"
    changed = {line for line, other in zip(old_lines, new_lines, strict=False) if line != other}
    assert changed == {
        "status: draft",
        "implementation_status: none",
        "updated: 2026-10-02",
        "last_reviewed: 2026-10-02",
    }

    # A header without `updated:` gains the field, appended once, last.
    moved_no_updated = (fx.archive / "2026-03-04-no-updated" / "spec.md").read_text(encoding="utf-8")
    _, original_header, original_tail = _meta(no_updated)
    _, new_header, new_tail = _meta(moved_no_updated)
    assert new_tail == original_tail
    expected = original_header.split("\n")
    expected[1] = "status: accepted"
    expected[2] = "implementation_status: done"
    expected[4] = f"last_reviewed: {DAY.isoformat()}"
    expected.append(f"updated: {DAY.isoformat()}")
    assert new_header.split("\n") == expected


# ---------------------------------------------------------------------------
# Criterion 5 — the index matches the registry generator afterwards
# ---------------------------------------------------------------------------


def test_index_matches_registry_after_archive(plans_repo: Fixture) -> None:
    fx = plans_repo
    fx.add("closed-one", files=_closed_files("b-closed"))
    # The one active fixture `check()` reads for age uses a date relative to
    # today: the registry's staleness finding measures `date.today()` against
    # `last_reviewed`, and a fixed 2026 date would drift past 90 days.
    recent = (dt.date.today() - dt.timedelta(days=2)).isoformat()
    fx.add(
        "open-two",
        files={
            "spec.md": _artefact("Spec — open thing", "b-open", date=recent, reviewed=recent),
            "plan.md": _artefact("Plan — open thing", "b-open", date=recent, reviewed=recent),
            "research.md": _artefact("Research — open thing", "b-open", date=recent, reviewed=recent),
        },
    )
    fx.add("archive/2026-01-01-older", files=_archived_files("b-closed"))
    fx.set_render({"b-closed": "closed", "b-open": "open"})

    assert archive.main(["--write"]) == 0

    index_text = (fx.root / "plans" / "INDEX.md").read_text(encoding="utf-8")
    assert index_text == reg.render_index(), "the index deviates from the registry generator's output"
    assert "archive/2026-03-04-closed-one/spec.md" in index_text
    assert "changes/closed-one/spec.md" not in index_text, "a stale source row remains"

    verdict = reg.check()
    assert verdict.exit_code(strict=True) == 0, verdict.render()
    assert "closed-one" not in verdict.render(), "the closed-active coupling still names the moved fixtures"


# ---------------------------------------------------------------------------
# Criterion 5 — moving does not exempt an invalid post-cutoff ledger
# ---------------------------------------------------------------------------


def test_archiving_does_not_exempt_criterion_ledger(plans_repo: Fixture, capsys: pytest.CaptureFixture[str]) -> None:
    fx = plans_repo
    plan_text = (
        _artefact("Plan — ledger", "b-ledger", date="2026-10-20", reviewed="2026-10-21", body="")
        + "## Criterion ledger\n"
        + "\n"
        + "- 1: not yet written tests/test_absent_proof.py::test_absent_proof — the proof is still owed\n"
    )
    spec_text = (
        _artefact("Spec — ledger", "b-ledger", body="")
        + "## Acceptance criteria\n"
        + "\n"
        + "1. One provable behaviour.\n"
    )
    fx.add(
        "ledger-one",
        files={
            "spec.md": spec_text,
            "plan.md": plan_text,
            "research.md": _artefact("Research — ledger", "b-ledger"),
        },
    )
    fx.set_render({"b-ledger": "closed"})

    assert check_criterion_ledger.run(fx.root) == 0, "the live plan's not-yet-written entry is accepted before the move"

    assert archive.main(["--write"]) == 0
    moved_plan = fx.archive / "2026-03-04-ledger-one" / "plan.md"
    assert moved_plan.is_file()

    assert check_criterion_ledger.run(fx.root) == 1, "archiving exempted an invalid post-cutoff ledger"
    assert "archive/2026-03-04-ledger-one/plan.md" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Criterion 6 — a preflight failure leaves the entire batch unchanged
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "case",
    ["broken-render", "empty-render", "duplicate-ids", "malformed-header", "existing-destination", "symlink-member"],
)
def test_preflight_failure_leaves_entire_batch_unchanged(
    plans_repo: Fixture, capsys: pytest.CaptureFixture[str], case: str
) -> None:
    fx = plans_repo
    fx.add("good-one", files=_closed_files("b-good"))
    fx.add("also-good", files=_closed_files("b-also"))
    rows = {"b-good": "closed", "b-also": "closed"}
    if case == "malformed-header":
        fx.add("bad-one", files={"spec.md": _artefact("Spec — bad", "b-bad"), "plan.md": "no front matter at all\n"})
        rows["b-bad"] = "closed"
    elif case == "existing-destination":
        occupied = fx.archive / "2026-03-04-good-one"
        occupied.mkdir()
        (occupied / "sentinel.txt").write_bytes(b"evidence")
    elif case == "symlink-member":
        fx.add("linked-one", files=_closed_files("b-link"), companions={"note.txt": b"n"})
        (fx.changes / "linked-one" / "link.txt").symlink_to(fx.changes / "linked-one" / "note.txt")
        rows["b-link"] = "closed"
    fx.set_render(rows)
    if case == "broken-render":
        fx.render_path.write_text("not json at all\n", encoding="utf-8")
    elif case == "empty-render":
        fx.render_path.write_text("", encoding="utf-8")
    elif case == "duplicate-ids":
        fx.render_path.write_text(
            json.dumps({"id": "b-good", "status": "closed"})
            + "\n"
            + json.dumps({"id": "b-good", "status": "open"})
            + "\n",
            encoding="utf-8",
        )

    before = _snapshot(fx.root)
    assert archive.main(["--write"]) == 1
    captured = capsys.readouterr()
    combined = captured.out + captured.err

    assert _snapshot(fx.root) == before, f"case {case} mutated the batch"
    if case == "broken-render":
        assert "cannot measure — nothing attempted" in combined
        assert "not valid" in combined
    elif case == "empty-render":
        assert "cannot measure — nothing attempted" in combined
    elif case == "duplicate-ids":
        assert "names bead 'b-good' twice" in combined
    elif case == "malformed-header":
        assert "write refused" in combined
        assert "blocked plans/changes/bad-one" in combined
        assert "has no readable front-matter block" in combined
    elif case == "existing-destination":
        assert "the destination already exists" in combined
        assert (fx.archive / "2026-03-04-good-one" / "sentinel.txt").read_bytes() == b"evidence"
    elif case == "symlink-member":
        assert "symlink inside the folder" in combined
    assert "archived plans/changes/good-one" not in combined, "a refusal still moved part of the batch"


# ---------------------------------------------------------------------------
# Criterion 7 — an I/O or index failure reports completed and unfinished work
# ---------------------------------------------------------------------------


def test_write_failure_reports_partial_work(
    plans_repo: Fixture, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fx = plans_repo
    fx.add("alpha", files=_closed_files("b-a"))
    fx.add("beta", files=_closed_files("b-b"))
    fx.set_render({"b-a": "closed", "b-b": "closed"})

    original = archive._relocate

    def _flaky(src: Path, dst: Path, artefacts: dict[Path, archive.Artefact], day: dt.date) -> None:
        if src.name == "beta":
            raise OSError("disk full during the move")
        original(src, dst, artefacts, day)

    monkeypatch.setattr(archive, "_relocate", _flaky)
    assert archive.main(["--write"]) == 1
    err = capsys.readouterr().err
    assert "FINISHED WITH FAILURES" in err
    assert "completed moves:" in err
    assert "plans/changes/alpha -> plans/changes/archive/2026-03-04-alpha" in err
    assert "unfinished work:" in err
    assert "beta" in err and "disk full during the move" in err
    assert "source left in place" in err
    assert (fx.changes / "beta" / "spec.md").is_file(), "the unfinished folder's source vanished"
    assert not (fx.archive / "2026-03-04-beta").exists(), "a partial destination was hidden instead of reported"
    assert (fx.archive / "2026-03-04-alpha" / "spec.md").is_file()
    # The index step follows the moves; a stopped run never reaches it, so no
    # half-moved tree is rendered into plans/INDEX.md.
    assert not (fx.root / "plans" / "INDEX.md").exists(), "a failed run rewrote the index"

    # The index stage itself failing is reported the same way.
    monkeypatch.setattr(archive, "_relocate", original)

    def _boom() -> str:
        raise OSError("index generation failed on purpose")

    monkeypatch.setattr(reg, "render_index", _boom)
    assert archive.main(["--write"]) == 1
    err = capsys.readouterr().err
    assert "completed moves:" in err
    assert "plans/changes/beta -> plans/changes/archive/2026-03-04-beta" in err
    assert "plans/INDEX.md: not regenerated" in err
    assert "the registry generator failed: index generation failed on purpose" in err
    assert (fx.archive / "2026-03-04-beta" / "spec.md").is_file()
    assert not (fx.changes / "beta").exists()
    assert not (fx.root / "plans" / "INDEX.md").exists(), "the failed run left a half-updated index"


# ---------------------------------------------------------------------------
# Criterion 8 — a successful repeat run is byte-identical
# ---------------------------------------------------------------------------


def test_successful_repeat_is_byte_identical(plans_repo: Fixture, capsys: pytest.CaptureFixture[str]) -> None:
    fx = plans_repo
    fx.add("once", files=_closed_files("b-once"), companions={"c.txt": b"keep"})
    fx.set_render({"b-once": "closed"})

    assert archive.main(["--write"]) == 0
    first = _snapshot(fx.root)
    assert archive.main(["--write"]) == 0
    assert "nothing to archive" in capsys.readouterr().out
    assert _snapshot(fx.root) == first, "the repeat run changed a byte"
    assert len([p for p in fx.archive.iterdir() if p.is_dir()]) == 1, "a second dated copy appeared"
    stamped = "\n".join(p.read_text(encoding="utf-8") for p in sorted((fx.archive / "2026-03-04-once").glob("*.md")))
    assert stamped.count(f"updated: {DAY.isoformat()}") == 3, "historical headers were restamped"


# ---------------------------------------------------------------------------
# Criterion 9 — the post-merge procedure orders archive after closure
# ---------------------------------------------------------------------------


def test_post_merge_procedure_orders_archive_after_closure() -> None:
    prompt = (REPO_ROOT / "prompts" / "07-commit.md").read_text(encoding="utf-8")
    if "make archive" not in prompt:
        pytest.skip(
            "plan step 5 (bootstrap) owns the held prompts/07-commit.md; this attempt must not "
            "depend on its future wording, so the real assertions wait for the bootstrap"
        )
    first_archive = prompt.index("make archive")
    first_close = prompt.index("close-merged")
    assert first_close < first_archive, "the archive step must follow the close-merged reconciliation"
    assert "make archive ARGS=--write" in prompt, "the write invocation is part of the procedure"
    assert "another session's checkout" not in prompt, "the procedure must never touch another session's checkout"
