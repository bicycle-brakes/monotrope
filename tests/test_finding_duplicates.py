"""The gate `finding-duplicates`: a new or changed duplicate row uses the canonical form.

Criterion 9 of plans/changes/findings-per-model/spec.md. Every repository a
test reads is built in `tmp_path`. Each test stands next to the fault that
turns it red.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import check_finding_duplicates as gate  # noqa: E402

IDENTITY = ["-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false"]
HEADER = "---\nstatus: draft\n---\n\n"
ROW = "| {id} | MAJOR | CODE | x.py | a finding | Codex | {status} |"


def git(root: Path, *args: str) -> str:
    command = ["git", "-C", str(root), *IDENTITY, *args]
    return subprocess.run(command, capture_output=True, text=True, check=True).stdout.strip()


def commit(root: Path, files: dict[str, str]) -> str:
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "step")
    return git(root, "rev-parse", "HEAD")


def table(*rows: tuple[str, str]) -> str:
    return "\n".join(ROW.format(id=row_id, status=status) for row_id, status in rows) + "\n"


def base_repo(tmp_path: Path, files: dict[str, str]) -> tuple[Path, str]:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q", "-b", "main")
    return root, commit(root, files)


PATH = "plans/changes/c1/findings.md"


def test_legacy_duplicate_reason_and_unparsed_id_fail_gate(tmp_path):
    import findings_reader as reader

    root, base = base_repo(tmp_path, {PATH: HEADER + table(("L1-1", "fixed"))})
    status = "rejected — same as L1-1: see L2-2"
    head = commit(root, {PATH: HEADER + table(("L1-1", "fixed"), ("L1-2", status))})
    assert any("L1-2" in item for item in gate.measure(root, base, head))
    assert reader.duplicate_targets(status) == ["L1-1"]
    result = reader.read_change(
        "c1", PATH, "## Phase 6 — Codex, 2026-11-01\n" + table(("L1-1", "fixed"), ("L1-2", status))
    )
    assert not result.gaps
    assert next(row for row in result.findings if row.id == "L1-2").duplicate
    assert gate.marks_duplicate("unreadable status mentioning L1-1")


def test_new_duplicate_form_gate(tmp_path):
    history = table(("L1-1", "fixed"), ("L1-2", "rejected — Same as L1-1"))
    root, base = base_repo(tmp_path, {PATH: HEADER + history})

    # a changed legacy row fails, an unchanged one is history
    legacy = commit(root, {PATH: HEADER + history + table(("L1-3", "rejected — Same as L1-1"))})
    found = gate.measure(root, base, legacy)
    assert len(found) == 1 and "L1-3" in found[0], "a new legacy duplicate form passed"
    assert all("L1-2" not in line for line in found), "an unchanged historical row was treated as new"

    edited = history.replace("Same as L1-1", "same as L1-1 again")
    changed = commit(root, {PATH: HEADER + edited + table(("L1-3", "open"))})
    assert any("L1-2" in line for line in gate.measure(root, base, changed)), "a changed legacy row passed"

    # the canonical forms pass, including several ids and a reason
    good = table(
        ("L1-3", "rejected — duplicate of L1-1"),
        ("L1-4", "rejected — duplicate of L1-1 and L1-3"),
        ("L1-5", "rejected — duplicate of L1-1: same shell"),
        ("L1-6", "rejected — not a repeat"),
    )
    canonical = commit(root, {PATH: HEADER + history + good})
    assert gate.measure(root, base, canonical) == [], "a valid canonical form or an ID-less marker failed"

    # a new findings file is checked whole
    added = commit(root, {"plans/changes/c2/findings.md": HEADER + table(("L1-1", "duplicate of L1-2"))})
    assert any("c2" in line for line in gate.measure(root, canonical, added)), "a new file was not checked"


def test_new_duplicate_form_gate_keeps_moved_rows(tmp_path):
    rows = [(f"L1-{number}", "fixed") for number in range(3, 30)]
    history = table(("L1-1", "fixed"), ("L1-2", "rejected — Same as L1-1"), *rows)
    root, base = base_repo(tmp_path, {PATH: HEADER + history})

    moved = "plans/changes/archive/2026-11-01-c1/findings.md"
    (root / moved).parent.mkdir(parents=True)
    git(root, "mv", PATH, moved)
    (root / moved).write_text(HEADER.replace("draft", "archived") + history, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "archive")
    head = git(root, "rev-parse", "HEAD")
    assert gate.measure(root, base, head) == [], "an unchanged archived row was treated as new"

    # a legacy row added in the moved file is still caught
    extended = HEADER.replace("draft", "archived") + history + table(("L1-99", "same as L1-1"))
    (root / moved).write_text(extended, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "new row")
    later = git(root, "rev-parse", "HEAD")
    assert any("L1-99" in line for line in gate.measure(root, base, later))


def test_unstaged_move_preserves_history_but_checks_new_rows(tmp_path):
    history = table(("L1-1", "fixed"), ("L1-2", "rejected — Same as L1-1"))
    root, base = base_repo(tmp_path, {PATH: HEADER + history})
    moved = root / "plans/changes/archive/c1/findings.md"
    moved.parent.mkdir(parents=True)
    (root / PATH).rename(moved)
    assert gate.measure(root, base) == [], "an unstaged move must preserve historical rows"
    moved.write_text(HEADER + history + table(("L1-3", "same as L1-1")), encoding="utf-8")
    found = gate.measure(root, base)
    assert len(found) == 1 and "L1-3" in found[0], "new rows in a moved file must still be checked"


def test_new_duplicate_form_gate_exit_codes(tmp_path, capsys):
    root, base = base_repo(tmp_path, {PATH: HEADER + table(("L1-1", "fixed"))})
    good = commit(root, {PATH: HEADER + table(("L1-1", "fixed"), ("L1-2", "rejected — duplicate of L1-1"))})
    assert gate.main(["--root", str(root), "--base", base, "--head", good]) == 0
    bad = commit(root, {PATH: HEADER + table(("L1-1", "fixed"), ("L1-2", "repeat of L1-1"))})
    assert gate.main(["--root", str(root), "--base", base, "--head", bad]) == 1
    assert "L1-2" in capsys.readouterr().out


def test_the_gate_goes_red_when_a_new_duplicate_row_uses_a_free_form(tmp_path, capsys):
    """The mutation evidence of the gate finding-duplicates (tests/test_ci.py ratchet).

    The fault seeded: one new row marks a duplicate in a free form instead of
    `rejected — duplicate of <ID>`. The gate must exit 1 and name the row.
    """
    root, base = base_repo(tmp_path, {PATH: HEADER + table(("L1-1", "fixed"))})
    bad = commit(root, {PATH: HEADER + table(("L1-1", "fixed"), ("L1-2", "rejected — same as L1-1"))})
    assert gate.main(["--root", str(root), "--base", base, "--head", bad]) == 1, "a free-form duplicate passed"
    assert "L1-2" in capsys.readouterr().out


def test_cannot_measure_exits_three(tmp_path):
    root, base = base_repo(tmp_path, {PATH: HEADER})
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts/check_finding_duplicates.py"),
            "--root",
            str(root),
            "--head",
            "missing",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 3, f"cannot-measure must exit 3, got {result.returncode}: {result.stderr}"


def test_only_added_occurrences_of_same_id_are_checked(tmp_path):
    history = table(("L1-1", "fixed"), ("L1-2", "rejected — Same as L1-1"))
    root, base = base_repo(tmp_path, {PATH: HEADER + history})
    head = commit(root, {PATH: HEADER + history + table(("L1-2", "fixed"))})
    assert gate.measure(root, base, head) == []
    bad = commit(root, {PATH: HEADER + history + table(("L1-3", "rejected — false: repeat of L1-1"))})
    assert any("L1-3" in item for item in gate.measure(root, base, bad))


def test_unknown_width_finding_row_is_reported(tmp_path):
    root, base = base_repo(tmp_path, {PATH: HEADER + table(("L1-1", "fixed"))})
    malformed = "| L1-2 | MAJOR | CODE | x.py | finding | reviewer | same as L1-1 | extra |\n"
    head = commit(root, {PATH: HEADER + table(("L1-1", "fixed")) + malformed})
    found = gate.measure(root, base, head)
    assert any("L1-2" in item and "width" in item for item in found)


def test_gate_checks_staged_unstaged_and_untracked_working_tree_rows(tmp_path, capsys):
    """F6-1: the local gate checks working-tree changes relative to the merge base before commit."""
    rows = [(f"L1-{number}", "fixed") for number in range(3, 30)]
    history = table(("L1-1", "fixed"), ("L1-2", "rejected — Same as L1-1"), *rows)
    root, _ = base_repo(tmp_path, {PATH: HEADER + history})

    # unstaged bad duplicate row fails, while unchanged historical L1-2 stays exempt
    bad_row = table(("L1-30", "rejected — same as L1-1"))
    (root / PATH).write_text(HEADER + history + bad_row, encoding="utf-8")
    assert gate.main(["--root", str(root)]) == 1, "an unstaged bad duplicate row passed"
    out = capsys.readouterr().out
    assert "L1-30" in out and "L1-2" not in out

    # staged bad duplicate row also fails
    git(root, "add", PATH)
    assert gate.main(["--root", str(root)]) == 1, "a staged bad duplicate row passed"
    out = capsys.readouterr().out
    assert "L1-30" in out and "L1-2" not in out

    # canonical replacement passes in working tree before commit
    good_row = table(("L1-30", "rejected — duplicate of L1-1"))
    (root / PATH).write_text(HEADER + history + good_row, encoding="utf-8")
    assert gate.main(["--root", str(root)]) == 0
    capsys.readouterr()

    # untracked findings.md with a bad duplicate row fails
    untracked = root / "plans/changes/c2/findings.md"
    untracked.parent.mkdir(parents=True, exist_ok=True)
    untracked.write_text(HEADER + table(("L1-1", "rejected — same as L1-2")), encoding="utf-8")
    assert gate.main(["--root", str(root)]) == 1, "an untracked bad duplicate row passed"
    out = capsys.readouterr().out
    assert "c2/findings.md:L1-1" in out
    untracked.unlink()

    # staged rename (archive) keeps historical rows exempt and catches a new bad row
    git(root, "checkout", "--", PATH)
    git(root, "reset", "-q", PATH)
    moved = "plans/changes/archive/2026-11-20-c1/findings.md"
    (root / moved).parent.mkdir(parents=True, exist_ok=True)
    git(root, "mv", PATH, moved)
    (root / moved).write_text(HEADER.replace("draft", "archived") + history, encoding="utf-8")
    assert gate.main(["--root", str(root)]) == 0, "an unchanged staged-archived row was treated as new"
    capsys.readouterr()
    (root / moved).write_text(
        HEADER.replace("draft", "archived") + history + table(("L1-99", "rejected — same as L1-1")),
        encoding="utf-8",
    )
    assert gate.main(["--root", str(root)]) == 1, "a new bad row in a staged-archived file passed"
    assert "L1-99" in capsys.readouterr().out
