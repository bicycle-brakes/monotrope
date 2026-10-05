"""The list behind the gate `research-currency`: research notes whose last review is too old.

Criteria 1-14 of plans/changes/research-currency/spec.md. Every test builds its own
tree in a temporary directory; the only files of this repository read are the ones that
travel with the kit (`decisions/gates.yaml`, the kit manifest). A test over this
repository's own notes would turn red on the day one of their reviews ages, and in the
kit probe's copy, which has no notes at all.

Each rule stands next to the fault that turns it red (docs/WORKFLOW.md, phase 5: a gate
that has never been red measures nothing). The faults planted for these tests, with the
test each one turned red, are recorded in plans/changes/research-currency/plan.md.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_research_currency.py"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "kit"))
import check_research_currency as cr  # noqa: E402
import ci_gates  # noqa: E402
import probe  # noqa: E402

TODAY = date(2026, 12, 20)
NOTES = "docs/research"
GATE_ID = "research-currency"


@pytest.fixture(autouse=True)
def _no_job_summary(monkeypatch: pytest.MonkeyPatch) -> None:
    """The hosted `verify` job sets GITHUB_STEP_SUMMARY; a test that calls `main` must not write into it."""
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def ago(days: int) -> date:
    return TODAY - timedelta(days=days)


def header(*lines: str) -> str:
    return "---\n" + "\n".join(lines) + "\n---\n\nBody.\n"


def reviewed(day: date) -> str:
    return header("title: A note", f"last_reviewed: {day}")


def put(root: Path, rel: str, content: str | bytes = "") -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
    return path


def put_note(root: Path, name: str, content: str | bytes) -> str:
    put(root, f"{NOTES}/{name}", content)
    return f"{NOTES}/{name}"


def run(
    root: Path,
    *args: str,
    today: str | None = "2026-12-20",
    env: dict[str, str] | None = None,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """The script as the nightly job runs it, with the clock and the summary file under control."""
    full_env = {k: v for k, v in os.environ.items() if k != "GITHUB_STEP_SUMMARY"}
    full_env["PYTHONIOENCODING"] = "utf-8"
    full_env.update(env or {})
    command = [sys.executable, str(SCRIPT), "--root", str(root)]
    if today is not None:
        command += ["--today", today]
    return subprocess.run(
        command + list(args), capture_output=True, text=True, encoding="utf-8", env=full_env, cwd=cwd, check=False
    )


def by_path(notes: list[cr.Note]) -> dict[str, cr.Note]:
    return {n.path: n for n in notes}


def tree_state(root: Path) -> dict[str, str]:
    """Every file and directory below `root` with a hash of its bytes: a change in any byte shows."""
    state: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        key = p.relative_to(root).as_posix()
        state[key] = "dir" if p.is_dir() else hashlib.sha256(p.read_bytes()).hexdigest()
    return state


# ---------------------------------------------------------------------------
# criterion 1 — the notes
# ---------------------------------------------------------------------------


def test_only_notes_under_docs_research_are_listed(tmp_path: Path) -> None:
    for rel in (
        "docs/research/_INDEX.md",
        "docs/research/_draft.md",
        "docs/research/sub/_INDEX.md",
        "docs/research/a.txt",
        "docs/research/a.md.bak",
        "docs/other/b.md",
        "docs/c.md",
        "README.md",
        "docs/research/sub/deep/c.md",
        "docs/research/d.md",
    ):
        put(tmp_path, rel, reviewed(ago(1)))
    (tmp_path / "docs/research/e.md").mkdir()  # a directory with a note's name is no note

    paths = [n.path for n in cr.measure(tmp_path, TODAY)]

    assert sorted(paths) == ["docs/research/d.md", "docs/research/sub/deep/c.md"]


# ---------------------------------------------------------------------------
# criterion 2 — the review date is `last_reviewed:` and nothing else
# ---------------------------------------------------------------------------


def test_the_review_date_is_last_reviewed_and_nothing_else(tmp_path: Path) -> None:
    put_note(
        tmp_path,
        "stale-but-edited.md",
        header(
            f"last_reviewed: {ago(200)}",
            f"updated: {ago(1)}",
            f"created: {ago(1)}",
            "review:",
            "  status: approved",
            f"  approved_at: {ago(1)}",
        ),
    )
    put_note(
        tmp_path,
        "fresh-but-old-edit.md",
        header(f"last_reviewed: {ago(5)}", f"updated: {ago(400)}", f"created: {ago(400)}"),
    )
    put_note(tmp_path, "nested-only.md", header("review:", f"  last_reviewed: {ago(1)}"))
    put_note(
        tmp_path, "top-and-nested.md", header(f"last_reviewed: {ago(150)}", "review:", f"  last_reviewed: {ago(1)}")
    )
    put_note(tmp_path, "double-quoted.md", header(f'last_reviewed: "{ago(30)}"'))
    put_note(tmp_path, "single-quoted.md", header(f"last_reviewed: '{ago(30)}'"))
    put_note(tmp_path, "commented.md", header(f"last_reviewed: {ago(30)}  # checked against the source"))

    notes = by_path(cr.measure(tmp_path, TODAY))

    stale = notes[f"{NOTES}/stale-but-edited.md"]
    assert (stale.due, stale.age_days, stale.problem) == (True, 200, None)
    fresh = notes[f"{NOTES}/fresh-but-old-edit.md"]
    assert (fresh.due, fresh.age_days, fresh.problem) == (False, 5, None)
    nested = notes[f"{NOTES}/nested-only.md"]
    assert (nested.due, nested.last_reviewed, nested.problem) == (True, None, "no last_reviewed")
    both = notes[f"{NOTES}/top-and-nested.md"]
    assert (both.due, both.age_days) == (True, 150)
    for name in ("double-quoted.md", "single-quoted.md", "commented.md"):
        usable = notes[f"{NOTES}/{name}"]
        assert (usable.last_reviewed, usable.age_days, usable.due, usable.problem) == (ago(30), 30, False, None), name


def test_a_header_with_a_byte_order_mark_and_crlf_line_endings_is_read(tmp_path: Path) -> None:
    text = f"﻿---\r\ntitle: A note\r\nlast_reviewed: {ago(40)}\r\n---\r\nBody\r\n"
    put_note(tmp_path, "windows.md", text.encode("utf-8"))

    (note,) = cr.measure(tmp_path, TODAY)

    assert (note.last_reviewed, note.problem) == (ago(40), None)


# ---------------------------------------------------------------------------
# criterion 3 — due by age
# ---------------------------------------------------------------------------


def test_the_list_notices_a_note_past_the_threshold(tmp_path: Path) -> None:
    """The mutation evidence of criterion 13: a due note that is not listed turns this red."""
    for days in (0, 89, 90, 91, 400):
        put_note(tmp_path, f"age-{days:03d}.md", reviewed(ago(days)))

    due = {Path(n.path).stem: n.due for n in cr.measure(tmp_path, TODAY)}

    assert due == {"age-000": False, "age-089": False, "age-090": False, "age-091": True, "age-400": True}
    out = run(tmp_path).stdout
    assert f"  due  {ago(91)}  91 days  {NOTES}/age-091.md\n" in out
    assert f"  due  {ago(400)}  400 days  {NOTES}/age-400.md\n" in out
    assert "age-090" not in out.split("oldest:")[0]


def test_the_threshold_is_one_named_constant(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert cr.STALE_AFTER_DAYS == 90
    for days in (29, 30, 31):
        put_note(tmp_path, f"age-{days}.md", reviewed(ago(days)))
    monkeypatch.setattr(cr, "STALE_AFTER_DAYS", 30)

    notes = cr.measure(tmp_path, TODAY)

    assert {Path(n.path).stem: n.due for n in notes} == {"age-29": False, "age-30": False, "age-31": True}
    assert "review more than 30 days before 2026-12-20" in cr.render_text(notes, TODAY)
    assert json.loads(cr.render_json(notes, TODAY))["threshold_days"] == 30


# ---------------------------------------------------------------------------
# criterion 4 — an unusable review date makes a note due, with the reason
# ---------------------------------------------------------------------------

NOT_A_MAPPING = "frontmatter is not a YAML mapping"


def _not_a_date(shown: str) -> str:
    return f"last_reviewed '{shown}' is not a YYYY-MM-DD date"


UNUSABLE: list[tuple[str, str | bytes, str]] = [
    ("no-header", "Just text, no header.\n", "no frontmatter"),
    ("unterminated-header", "---\nlast_reviewed: 2026-12-01\n", "no frontmatter"),
    ("header-is-a-list", "---\n- a\n- b\n---\n\nBody\n", NOT_A_MAPPING),
    ("header-is-a-scalar", "---\njust words\n---\n\nBody\n", NOT_A_MAPPING),
    ("header-does-not-parse", "---\nkey: [unclosed\n---\n\nBody\n", NOT_A_MAPPING),
    ("impossible-date-by-tag", header("last_reviewed: !!timestamp 2026-02-30"), NOT_A_MAPPING),
    ("no-key", header("title: A note", f"updated: {ago(1)}"), "no last_reviewed"),
    ("empty-value", header("last_reviewed:"), "last_reviewed is empty"),
    ("empty-string", header("last_reviewed: ''"), "last_reviewed is empty"),
    ("null-value", header("last_reviewed: null"), "last_reviewed is empty"),
    ("tilde-value", header("last_reviewed: ~"), "last_reviewed is empty"),
    ("a-word", header("last_reviewed: soon"), _not_a_date("soon")),
    ("impossible-date", header("last_reviewed: 2026-02-30"), _not_a_date("2026-02-30")),
    ("month-13", header("last_reviewed: 2026-13-01"), _not_a_date("2026-13-01")),
    ("compact-date", header("last_reviewed: 20261201"), _not_a_date("20261201")),
    ("compact-date-quoted", header("last_reviewed: '20261201'"), _not_a_date("20261201")),
    ("short-month", header("last_reviewed: 2026-9-6"), _not_a_date("2026-9-6")),
    ("slashes", header("last_reviewed: 2026/12/01"), _not_a_date("2026/12/01")),
    ("timestamp", header("last_reviewed: 2026-12-01 10:00:00"), _not_a_date("2026-12-01 10:00:00")),
    ("timestamp-utc", header("last_reviewed: 2026-12-01T10:00:00Z"), _not_a_date("2026-12-01T10:00:00Z")),
    ("a-number", header("last_reviewed: 7"), _not_a_date("7")),
    ("a-boolean", header("last_reviewed: true"), _not_a_date("True")),
    ("a-list", header("last_reviewed: [2026-12-01]"), _not_a_date("['2026-12-01']")),
    (
        "two-days-ahead",
        header(f"last_reviewed: {TODAY + timedelta(days=2)}"),
        "last_reviewed 2026-12-22 is in the future",
    ),
    ("far-future", header("last_reviewed: 2099-01-01"), "last_reviewed 2099-01-01 is in the future"),
    ("not-utf-8", b"---\nlast_reviewed: 2026-12-01\n---\n\xff\xfe\n", "not valid UTF-8"),
]


@pytest.mark.parametrize(("name", "content", "reason"), UNUSABLE, ids=[u[0] for u in UNUSABLE])
def test_an_unusable_review_date_is_due_with_its_reason(
    tmp_path: Path, name: str, content: str | bytes, reason: str
) -> None:
    bad = put_note(tmp_path, f"{name}.md", content)
    good = put_note(tmp_path, "zz-good.md", reviewed(ago(5)))

    notes = cr.measure(tmp_path, TODAY)

    found = by_path(notes)[bad]
    assert (found.due, found.last_reviewed, found.age_days, found.problem) == (True, None, None, reason)
    assert notes[0].path == bad  # unusable first
    assert by_path(notes)[good].problem is None  # the run went on to the next note


def test_a_note_that_cannot_be_read_is_due_with_its_reason(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    locked = put_note(tmp_path, "locked.md", reviewed(ago(1)))
    good = put_note(tmp_path, "open.md", reviewed(ago(1)))
    real = Path.read_bytes

    def deny(self: Path) -> bytes:
        if self.name == "locked.md":
            raise PermissionError(13, "Permission denied")
        return real(self)

    monkeypatch.setattr(Path, "read_bytes", deny)

    notes = by_path(cr.measure(tmp_path, TODAY))

    assert notes[locked].problem == "cannot be read (Permission denied)"
    assert notes[locked].due is True
    assert notes[good].problem is None


def test_a_date_on_the_next_day_is_usable(tmp_path: Path) -> None:
    tomorrow = put_note(tmp_path, "tomorrow.md", reviewed(TODAY + timedelta(days=1)))
    after = put_note(tmp_path, "day-after.md", reviewed(TODAY + timedelta(days=2)))

    notes = by_path(cr.measure(tmp_path, TODAY))

    assert (notes[tomorrow].problem, notes[tomorrow].due, notes[tomorrow].age_days) == (None, False, -1)
    assert notes[after].problem == "last_reviewed 2026-12-22 is in the future"


def test_a_reason_is_one_short_line(tmp_path: Path) -> None:
    put_note(tmp_path, "multi.md", header('last_reviewed: "line one\\nline two"'))
    put_note(tmp_path, "long.md", header(f"last_reviewed: {'x' * 300}"))

    notes = by_path(cr.measure(tmp_path, TODAY))

    assert notes[f"{NOTES}/multi.md"].problem == _not_a_date("line one line two")
    long_reason = notes[f"{NOTES}/long.md"].problem or ""
    assert "…" in long_reason
    assert len(long_reason) < 150
    assert "\n" not in long_reason


# ---------------------------------------------------------------------------
# criterion 5 — the order
# ---------------------------------------------------------------------------


def _order_tree(root: Path) -> list[str]:
    """A tree whose files are created, and aged by mtime, in the reverse of the expected order."""
    expected = [
        put_note(root, "a-empty.md", header("last_reviewed:")),
        put_note(root, "z-nokey.md", header("title: no review date")),
        put_note(root, "a-2.md", reviewed(date(2026, 9, 1))),
        put_note(root, "b-1.md", reviewed(date(2026, 9, 1))),
        put_note(root, "sub/c.md", reviewed(date(2026, 9, 1))),
        put_note(root, "mid.md", reviewed(date(2026, 12, 10))),
        put_note(root, "new.md", reviewed(date(2026, 12, 19))),
    ]
    # The first in the expected order gets the newest mtime: any mtime order would be the wrong one.
    for step, rel in enumerate(expected):
        os.utime(root / rel, (1_700_000_000 - step * 1000, 1_700_000_000 - step * 1000))
    return expected


def test_unusable_first_then_oldest_then_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    expected = _order_tree(tmp_path)
    real_rglob = Path.rglob

    assert [n.path for n in cr.measure(tmp_path, TODAY)] == expected
    # Whatever order the file system hands the files over in, the output order is the same.
    monkeypatch.setattr(Path, "rglob", lambda self, pattern: iter(sorted(real_rglob(self, pattern))))
    assert [n.path for n in cr.measure(tmp_path, TODAY)] == expected
    monkeypatch.setattr(Path, "rglob", lambda self, pattern: iter(sorted(real_rglob(self, pattern), reverse=True)))
    assert [n.path for n in cr.measure(tmp_path, TODAY)] == expected


def test_two_runs_give_the_same_bytes(tmp_path: Path) -> None:
    _order_tree(tmp_path)

    first = [run(tmp_path, "--format", fmt).stdout for fmt in ("text", "json")]
    for p in tmp_path.rglob("*.md"):
        os.utime(p, (1_600_000_000, 1_600_000_000))  # the same bytes, other mtimes
    second = [run(tmp_path, "--format", fmt).stdout for fmt in ("text", "json")]

    assert first == second
    assert all(first)


# ---------------------------------------------------------------------------
# criterion 6 — the day of the run
# ---------------------------------------------------------------------------

# POSIX TZ strings: the sign is inverted, `XXX-14` is UTC+14. Of the two zones one always
# stands on another calendar date than UTC, so a run that counts to the UTC date is caught.
ZONES = [("XXX-14", 14), ("XXX+12", -12)]


@pytest.mark.parametrize(("posix_tz", "offset_hours"), ZONES)
def test_without_today_the_local_date_counts(tmp_path: Path, posix_tz: str, offset_hours: int) -> None:
    before = (datetime.now(UTC) + timedelta(hours=offset_hours)).date()
    put_note(tmp_path, "old.md", reviewed(before - timedelta(days=95)))
    put_note(tmp_path, "new.md", reviewed(before - timedelta(days=5)))

    proc = run(tmp_path, "--format", "json", today=None, env={"TZ": posix_tz})
    after = (datetime.now(UTC) + timedelta(hours=offset_hours)).date()

    assert proc.returncode == 0, proc.stdout + proc.stderr
    doc = json.loads(proc.stdout)
    assert doc["today"] in {before.isoformat(), after.isoformat()}
    counted_to = date.fromisoformat(doc["today"])
    ages = {n["path"]: n["age_days"] for n in doc["notes"]}
    assert ages[f"{NOTES}/old.md"] == (counted_to - (before - timedelta(days=95))).days
    assert [n["due"] for n in doc["notes"]] == [True, False]


@pytest.mark.parametrize("posix_tz", [z for z, _ in ZONES])
def test_today_names_the_day_whatever_the_clock_says(tmp_path: Path, posix_tz: str) -> None:
    put_note(tmp_path, "x.md", reviewed(ago(95)))

    proc = run(tmp_path, today="2026-12-20", env={"TZ": posix_tz})

    assert proc.stdout == (
        f"research-currency: 1 note under docs/research/, 1 due (review more than 90 days before 2026-12-20)\n"
        f"  due  {ago(95)}  95 days  {NOTES}/x.md\n"
        f"oldest: {NOTES}/x.md, reviewed {ago(95)}, 95 days ago\n"
    )


@pytest.mark.parametrize("value", ["2026-13-01", "20261220", "2026-1-2", "yesterday", ""])
def test_a_malformed_today_is_a_usage_error(tmp_path: Path, value: str) -> None:
    put_note(tmp_path, "x.md", reviewed(ago(1)))

    proc = run(tmp_path, today=value)

    assert proc.returncode == 2
    assert proc.stdout == ""


# ---------------------------------------------------------------------------
# criterion 7 — the text output
# ---------------------------------------------------------------------------


def _mixed_tree(root: Path) -> None:
    put_note(root, "x.md", reviewed(ago(95)))
    put_note(root, "y.md", header("title: no review date"))
    put_note(root, "z.md", reviewed(ago(10)))


def test_the_text_has_a_line_per_due_note(tmp_path: Path) -> None:
    _mixed_tree(tmp_path)

    proc = run(tmp_path)

    assert proc.returncode == 0
    assert proc.stdout == (
        "research-currency: 3 notes under docs/research/, 2 due (review more than 90 days before 2026-12-20)\n"
        f"  due  no date  {NOTES}/y.md — no last_reviewed\n"
        f"  due  {ago(95)}  95 days  {NOTES}/x.md\n"
        f"oldest: {NOTES}/y.md, no usable review date (no last_reviewed)\n"
    )


def test_the_text_names_the_oldest_even_when_none_is_due(tmp_path: Path) -> None:
    put_note(tmp_path, "b.md", reviewed(ago(19)))
    put_note(tmp_path, "a.md", reviewed(ago(19)))
    put_note(tmp_path, "c.md", reviewed(ago(2)))

    proc = run(tmp_path)

    assert proc.stdout == (
        "research-currency: 3 notes under docs/research/, 0 due (review more than 90 days before 2026-12-20)\n"
        f"oldest: {NOTES}/a.md, reviewed {ago(19)}, 19 days ago\n"
    )


def test_the_oldest_line_reads_naturally_for_today_and_tomorrow(tmp_path: Path) -> None:
    put_note(tmp_path, "a.md", reviewed(TODAY))
    assert run(tmp_path).stdout.endswith(f"oldest: {NOTES}/a.md, reviewed {TODAY}, today\n")

    put_note(tmp_path, "a.md", reviewed(TODAY + timedelta(days=1)))
    assert run(tmp_path).stdout.endswith(f"oldest: {NOTES}/a.md, reviewed {TODAY + timedelta(days=1)}, tomorrow\n")

    put_note(tmp_path, "a.md", reviewed(ago(1)))
    assert run(tmp_path).stdout.endswith(f"oldest: {NOTES}/a.md, reviewed {ago(1)}, 1 day ago\n")


# ---------------------------------------------------------------------------
# criterion 8 — the JSON output
# ---------------------------------------------------------------------------


def test_the_json_carries_every_note_in_order(tmp_path: Path) -> None:
    put_note(tmp_path, "z-bald.md", header('last_reviewed: "bald — ä"'))
    put_note(tmp_path, "old.md", reviewed(ago(95)))
    put_note(tmp_path, "edge.md", reviewed(ago(90)))
    put_note(tmp_path, "tomorrow.md", reviewed(TODAY + timedelta(days=1)))
    put_note(tmp_path, "sub/deep.md", reviewed(ago(3)))

    proc = run(tmp_path, "--format", "json")

    assert proc.returncode == 0
    doc = json.loads(proc.stdout)
    assert list(doc) == ["schema_version", "today", "threshold_days", "corpus", "notes"]
    assert all(list(n) == ["path", "last_reviewed", "age_days", "due", "problem"] for n in doc["notes"])
    assert doc == {
        "schema_version": 1,
        "today": "2026-12-20",
        "threshold_days": 90,
        "corpus": "docs/research/",
        "notes": [
            {
                "path": f"{NOTES}/z-bald.md",
                "last_reviewed": None,
                "age_days": None,
                "due": True,
                "problem": "last_reviewed 'bald — ä' is not a YYYY-MM-DD date",
            },
            {"path": f"{NOTES}/old.md", "last_reviewed": str(ago(95)), "age_days": 95, "due": True, "problem": None},
            {"path": f"{NOTES}/edge.md", "last_reviewed": str(ago(90)), "age_days": 90, "due": False, "problem": None},
            {
                "path": f"{NOTES}/sub/deep.md",
                "last_reviewed": str(ago(3)),
                "age_days": 3,
                "due": False,
                "problem": None,
            },
            {
                "path": f"{NOTES}/tomorrow.md",
                "last_reviewed": str(TODAY + timedelta(days=1)),
                "age_days": -1,
                "due": False,
                "problem": None,
            },
        ],
    }
    assert "ä" in proc.stdout  # not escaped


# ---------------------------------------------------------------------------
# criterion 9 — the job summary
# ---------------------------------------------------------------------------


def test_the_summary_is_written_only_when_asked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "repo"
    _mixed_tree(root)
    summary = tmp_path / "summary.md"
    summary.write_text("an earlier step\n", encoding="utf-8")

    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    assert cr.main(["--root", str(root), "--today", "2026-12-20"]) == 0

    assert summary.read_text(encoding="utf-8") == (
        "an earlier step\n"
        "### Research currency\n\n"
        "3 notes under docs/research/, 2 due (review more than 90 days before 2026-12-20).\n\n"
        "| Reviewed | Days | Note |\n"
        "| --- | --- | --- |\n"
        f"| no date | — | `{NOTES}/y.md` — no last_reviewed |\n"
        f"| {ago(95)} | 95 | `{NOTES}/x.md` |\n\n"
        f"Oldest: {NOTES}/y.md, no usable review date (no last_reviewed).\n\n"
    )
    assert "research-currency: 3 notes" in capsys.readouterr().out  # the log still has it

    monkeypatch.delenv("GITHUB_STEP_SUMMARY")
    elsewhere = tmp_path / "cwd"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    before = tree_state(tmp_path)
    assert cr.main(["--root", str(root), "--today", "2026-12-20"]) == 0
    assert tree_state(tmp_path) == before


def test_the_summary_has_a_table_only_when_a_note_is_due(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    put_note(tmp_path, "a.md", reviewed(ago(19)))
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))

    assert cr.main(["--root", str(tmp_path), "--today", "2026-12-20"]) == 0

    assert summary.read_text(encoding="utf-8") == (
        "### Research currency\n\n"
        "1 note under docs/research/, 0 due (review more than 90 days before 2026-12-20).\n\n"
        f"Oldest: {NOTES}/a.md, reviewed {ago(19)}, 19 days ago.\n\n"
    )


def test_the_summary_carries_the_not_measured_line(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))

    assert cr.main(["--root", str(tmp_path / "empty"), "--today", "2026-12-20"]) == 3

    text = summary.read_text(encoding="utf-8")
    assert text.startswith("### Research currency\n\nresearch-currency: not measured — ")


def test_an_unwritable_summary_does_not_end_the_run(tmp_path: Path) -> None:
    put_note(tmp_path, "a.md", reviewed(ago(95)))

    proc = run(tmp_path, env={"GITHUB_STEP_SUMMARY": str(tmp_path)})  # a directory cannot be appended to

    assert proc.returncode == 0
    assert proc.stdout.startswith("research-currency: 1 note")
    assert "cannot write the job summary" in proc.stderr


# ---------------------------------------------------------------------------
# criterion 10 — never red over its content
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("fmt", ["text", "json"])
def test_due_notes_never_turn_the_run_red(tmp_path: Path, fmt: str) -> None:
    for i in range(5):
        put_note(tmp_path, f"old-{i}.md", reviewed(ago(100 + i)))
    put_note(tmp_path, "bad.md", header("last_reviewed: soon"))
    put_note(tmp_path, "binary.md", b"\xff\xfe\x00")

    proc = run(tmp_path, "--format", fmt)

    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stderr == ""


@pytest.mark.parametrize("fmt", ["text", "json"])
@pytest.mark.parametrize(
    ("setup", "reason"),
    [
        ("missing", "is not a directory"),
        ("a-file", "is not a directory"),
        ("empty", "holds no note"),
        ("only-index", "holds no note"),
        ("only-other-files", "holds no note"),
    ],
)
def test_a_missing_or_empty_corpus_is_not_measured(tmp_path: Path, setup: str, reason: str, fmt: str) -> None:
    if setup == "a-file":
        put(tmp_path, NOTES, "not a directory")
    elif setup == "empty":
        (tmp_path / NOTES).mkdir(parents=True)
    elif setup == "only-index":
        put(tmp_path, f"{NOTES}/_INDEX.md", reviewed(ago(1)))
    elif setup == "only-other-files":
        put(tmp_path, f"{NOTES}/notes.txt", "text")
        put(tmp_path, "docs/other.md", reviewed(ago(1)))

    proc = run(tmp_path, "--format", fmt)

    assert proc.returncode == 3
    assert proc.stdout.startswith("research-currency: not measured")
    assert reason in proc.stdout
    assert proc.stderr == ""


# ---------------------------------------------------------------------------
# criterion 11 — it only reads
# ---------------------------------------------------------------------------


def test_the_run_changes_no_byte_and_needs_no_git(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _mixed_tree(root)
    put(root, "docs/other.md", "outside")
    put_note(root, "binary.md", b"\xff\xfe")
    no_tools = tmp_path / "no-tools"
    no_tools.mkdir()
    before = tree_state(tmp_path)

    for fmt in ("text", "json"):
        # An empty PATH: a call of git, or of anything else, cannot start.
        proc = run(root, "--format", fmt, env={"PATH": str(no_tools)}, cwd=tmp_path)
        assert proc.returncode == 0, proc.stdout + proc.stderr

    assert tree_state(tmp_path) == before
    assert not (root / ".git").exists()  # not a git work tree, and it stayed one


# ---------------------------------------------------------------------------
# criteria 12-14 — the gate, the ratchets, the kit
# ---------------------------------------------------------------------------


def _gate() -> dict:
    (entry,) = [g for g in ci_gates.gates() if g["id"] == GATE_ID]
    return entry


def test_the_gate_reports_in_the_drift_job_only() -> None:
    gate = _gate()

    assert gate["command"] == "python3 scripts/check_research_currency.py"
    assert (gate["job"], gate["enforcement"], gate["floor"], gate["placement"]) == ("drift", "report", False, "both")
    assert (gate["needs_tracker"], gate["needs_history"]) == (False, False)
    assert "report is the level the maintainer chose" in gate["reason"]
    assert "not a step towards block" in gate["reason"]

    jobs = yaml.safe_load(ci_gates.generate_ci())["jobs"]
    drift_steps = {s.get("id"): s for s in jobs["drift"]["steps"]}
    assert drift_steps[GATE_ID]["run"] == gate["command"]
    assert drift_steps[GATE_ID]["continue-on-error"] is True
    assert GATE_ID not in {s.get("id") for s in jobs["verify"]["steps"]}


def test_the_kit_carries_the_script_and_its_test() -> None:
    for path in ("scripts/check_research_currency.py", "tests/test_research_currency.py"):
        found = probe.rolle(path)
        assert found is not None, f"{path} has no role in scripts/kit/manifest.yaml"
        assert found[0] == "mechanismus", path
