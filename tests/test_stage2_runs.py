"""The run counter of stage 2 - and the cases in which its numbers hold.

`scripts/stage2_runs.py` reads what `scripts/stage2.py` wrote into a change
folder and counts it (plans/changes/archive/2026-10-08-stage2-runs-count/spec.md). Every case
builds a small repository in `tmp_path` with rows rendered by the runner's own
`render_table` and column constants, so a fixture has the shape the runner
writes. Each test names the fault that turns it red; the plan's time log says
that each was planted once.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import pytest  # noqa: E402
import stage2  # noqa: E402
import stage2_runs  # noqa: E402

HEADER = "---\ntitle: x\n---\n\n# Findings\n"
ENDPOINTS = """\
endpunkte:
  - name: openai-codex
    residenz: anbieter-erklaert
    darf_sehen: [framework]
    modelle: [gpt-6.1-sol]
  - name: glm-coding-plan
    residenz: anbieter-erklaert
    darf_sehen: [framework]
    modelle: [glm-5.3, glm-5.3-flash]
"""


def call(verb: str, clean: bool = True) -> str:
    check = "leak check clean over 1 files, 2 commits, 3 rules." if clean else "leak check BLOCK."
    return f"Stage-2 call, 2026-10-08: {verb} · endpoint openai-codex · model gpt-6.1-sol · {check}"


def codex_rows(*rows: tuple[str, str, str, str]) -> str:
    """Rows of nine cells: (id, severity, status, broke)."""
    body = [[i, sev, "SPEC", "base", "`x.py`", "a finding", "Codex", status, broke] for i, sev, status, broke in rows]
    return stage2.render_table(stage2.ROW_COLUMNS, body)


def loop_rows(*rows: tuple[str, str, str, str]) -> str:
    """Released rows of ten cells: (id, status, broke, mark)."""
    body = [
        [i, "MINOR", "MAINT", "base", "`x.py`", "a finding", "GLM", status, broke, mark]
        for i, status, broke, mark in rows
    ]
    return stage2.render_table(stage2.RELEASED_COLUMNS, body)


def make_repo(root: Path, folders: dict[str, dict[str, str]], endpoints: str = ENDPOINTS) -> Path:
    for folder, files in folders.items():
        for name, text in files.items():
            path = root / folder / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    (root / "model-endpoints.yaml").write_text(endpoints, encoding="utf-8")
    return root


def run(root: Path, *args: str, capsys) -> tuple[int, str, str]:
    code = stage2_runs.main([*args, "--root", str(root)])
    out, err = capsys.readouterr()
    return code, out, err


def table_row(out: str, change: str) -> list[str]:
    line = next(line for line in out.splitlines() if line.startswith(f"| `{change}`"))
    return stage2.split_row(line)


SIMPLE = HEADER + "\n" + call("review") + "\n"


def test_an_active_and_an_archived_change_are_both_found(tmp_path: Path, capsys) -> None:
    """Fault: the archive not searched, or a suffix match taking `…-other-x` for `x` (criterion 1)."""
    make_repo(
        tmp_path,
        {
            "plans/changes/live": {"findings.md": SIMPLE},
            "plans/changes/archive/2026-10-01-old": {"findings.md": SIMPLE},
            "plans/changes/archive/2026-10-01-other-x": {"findings.md": SIMPLE},
        },
    )
    code, out, _ = run(tmp_path, "live", "old", capsys=capsys)
    assert code == 0
    assert "(`plans/changes/live`)" in table_row(out, "live")[0]
    assert "(`plans/changes/archive/2026-10-01-old`)" in table_row(out, "old")[0]
    code, out, err = run(tmp_path, "x", capsys=capsys)
    assert code == 2 and out == "" and "x: no findings.md" in err


def test_a_change_without_findings_or_with_two_archives_exits_2_and_prints_no_table(tmp_path: Path, capsys) -> None:
    """Fault: an empty row printed with exit 0, or the first of two archives taken (criterion 2)."""
    make_repo(
        tmp_path,
        {
            "plans/changes/live": {"findings.md": SIMPLE},
            "plans/changes/empty": {"research.md": "x\n"},
            "plans/changes/archive/2026-10-01-twice": {"findings.md": SIMPLE},
            "plans/changes/archive/2026-10-02-twice": {"findings.md": SIMPLE},
        },
    )
    for name, says in (
        ("empty", "no findings.md"),
        ("twice", "more than one archived folder"),
        ("Bad/name", "not a change name"),
    ):
        code, out, err = run(tmp_path, "live", name, capsys=capsys)
        assert (code, out) == (2, ""), name
        assert says in err, name


def test_loop_rows_are_taken_rejected_or_undecided_and_none_is_dropped() -> None:
    """Fault: a `rejected` row counted as taken, or an undecided row in no count (criterion 3)."""
    text = (
        HEADER
        + f"\n{stage2.RELEASE_HEADING} 2026-10-08\n\n"
        + loop_rows(
            ("L1-1", "taken — a test", "no", "agree"),
            ("L1-2", "rejected — out of scope", "", "agree"),
            ("L2-1", "Rejected — capitalised", "", "agree"),
            ("L2-2", "open", "", "—"),
        )
        + "\n\nRounds run: 2\n"
    )
    counts = stage2_runs.measure(text)
    assert (counts.taken, counts.rejected, counts.undecided) == (1, 2, 1)


def test_a_fixed_loop_row_counts_as_taken() -> None:
    """Fault: a `fixed` row counted as undecided, or not counted (criterion 27)."""
    text = (
        HEADER
        + f"\n{stage2.RELEASE_HEADING} 2026-10-08\n\n"
        + loop_rows(
            ("L1-1", "taken — t", "no", "agree"),
            ("L1-2", "fixed — tests/test_x.py::test_x", "no", "agree"),
            ("L1-3", "fixed — tests/test_x.py::test_x", "", "agree"),
        )
        + "\n\nRounds run: 1\n"
    )
    counts = stage2_runs.measure(text)
    assert (counts.taken, counts.undecided, counts.loop_rows) == (3, 0, 3)


def test_a_yes_in_any_table_counts_as_a_broken_test() -> None:
    """Fault: only loop rows read for `Broke a test`, or `no` counted (criterion 4)."""
    text = (
        HEADER
        + "\n## Phase 2a — Codex, 2026-10-08\n\n"
        + codex_rows(("F-1", "MAJOR", "in spec — x", "yes"))
        + "\n\n## Phase 6 — Codex, 2026-10-08\n\n"
        + codex_rows(("F-2", "BLOCKER", "closed — x", "YES"), ("F-3", "BLOCKER", "closed — x", "no"))
        + f"\n\n{stage2.RELEASE_HEADING} 2026-10-08\n\n"
        + loop_rows(("L1-1", "taken — t", "yes", "agree"), ("L1-2", "taken — t", "no", "agree"))
        + "\n"
    )
    assert stage2_runs.measure(text).broke == 3


def test_phase_6_rounds_are_verdict_lines_and_rows_count_by_their_section() -> None:
    """Fault: rounds read from `Rounds run:`, or a phase-2a row counted as phase 6 (criterion 5)."""
    text = (
        HEADER
        + "\n## Phase 2a — Codex, 2026-10-07\n\n"
        + codex_rows(("F-1", "MAJOR", "in spec", "—"), ("F-2", "MINOR", "in spec", "—"))
        + "\n\n## Phase 6 — Codex, 2026-10-08\n\n"
        + codex_rows(("F-3", "BLOCKER", "closed", "no"), ("F-4", "BLOCKER", "closed", "no"))
        + "\n\nPhase 6 verdict: codex abc, 2026-10-08\n"
        + f"\n{stage2.RELEASE_HEADING} 2026-10-08\n\n"
        + loop_rows(("L1-1", "taken — t", "no", "agree"))
        + "\n\nRounds run: 2\n"
        + "\n## Phase 6 — Codex, 2026-10-08\n\n"
        + codex_rows(("F-5", "MAJOR", "closed", "no"))
        + "\n\nPhase 6 verdict: codex abc, 2026-10-08\n"
    )
    counts = stage2_runs.measure(text)
    assert counts.rounds == 2
    assert stage2_runs.severities(counts.spec_review) == "1 MAJOR, 1 MINOR"
    assert stage2_runs.severities(counts.phase6) == "2 BLOCKER, 1 MAJOR"
    assert stage2_runs.severities(stage2_runs.Counter()) == "none"


def test_only_marks_that_start_disagree_are_counted() -> None:
    """Fault: every filled `Phase 6` cell counted, or `agree` matched inside `disagree` (criterion 6)."""
    text = (
        HEADER
        + f"\n{stage2.RELEASE_HEADING} 2026-10-08\n\n"
        + loop_rows(
            ("L1-1", "taken — t", "no", "agree"),
            ("L1-2", "taken — t", "no", "disagree — no fault"),
            ("L1-3", "rejected — r", "", "agree — I disagree with nothing"),
        )
        + "\n"
    )
    counts = stage2_runs.measure(text)
    assert (counts.disagree, counts.loop_rows) == (1, 3)


def test_calls_come_from_findings_and_research_and_only_clean_lines_count_clean() -> None:
    """Fault: research.md not read, a session line missed, or a blocked line counted clean (criterion 7)."""
    findings = (
        HEADER
        + "\n"
        + call("review-loop")
        + "\n\n"
        + call("review", clean=False)
        + "\n\nStage-2 session, 2026-10-08: attempt 1 · model gpt-6.1-sol · endpoint openai-codex · handover h.md · "
        "leak check clean over 1 files, 2 commits, 3 rules · dispatch accepted.\n"
        + "\nA prose line that mentions Stage-2 call, 2026-10-08: review is not a call.\n"
    )
    research = "Stage-2 call, 2026-10-08: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1 files, 2 commits, 3 rules.\n"
    counts = stage2_runs.measure(findings, research)
    assert counts.calls == [("review-loop", True), ("review", False), ("session", True), ("explore", True)]
    assert stage2_runs.calls_line("c", counts) == "- `c`: review-loop 1, review 1, session 1, explore 1 — 3 of 4 clean"


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_rev_reads_every_file_from_that_commit(tmp_path: Path, capsys) -> None:
    """Fault: `--rev` reading the working tree, or the cell not naming the commit (criterion 8)."""
    make_repo(tmp_path, {"plans/changes/archive/2026-10-01-run": {"findings.md": SIMPLE}})
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "one")
    first = _git(tmp_path, "rev-parse", "--short", "HEAD")
    findings = tmp_path / "plans/changes/archive/2026-10-01-run/findings.md"
    findings.write_text(SIMPLE + "\n" + call("review") + "\n", encoding="utf-8")
    (tmp_path / "model-endpoints.yaml").write_text("endpunkte: []\n", encoding="utf-8")

    code, out, _ = run(tmp_path, "run", "--rev", first, capsys=capsys)
    assert code == 0
    cells = table_row(out, "run")
    assert cells[1] == f"`{first}`" and cells[-1] == "1 / 1"
    assert "3 of 3 foreign routes cleared" in out

    code, out, _ = run(tmp_path, "run", capsys=capsys)
    cells = table_row(out, "run")
    assert cells[1] == f"tree at `{first}`" and cells[-1] == "2 / 2"
    assert "0 of 3 foreign routes cleared" in out

    code, out, err = run(tmp_path, "run", "--rev", "no-such-rev", capsys=capsys)
    assert (code, out) == (2, "") and "no-such-rev" in err


def test_criterion_4_counts_only_cleared_routes_and_no_cost_figure_is_printed(tmp_path: Path, capsys) -> None:
    """Fault: a route without residency counted cleared, or a number beside tokens and cost (criterion 9)."""
    no_residency = ENDPOINTS.replace(
        "    residenz: anbieter-erklaert\n    darf_sehen: [framework]\n    modelle: [glm",
        "    residenz: nicht-erklaert\n    darf_sehen: [framework]\n    modelle: [glm",
    )
    assert no_residency != ENDPOINTS
    make_repo(tmp_path, {"plans/changes/run": {"findings.md": SIMPLE}}, endpoints=no_residency)
    code, out, _ = run(tmp_path, "run", capsys=capsys)
    assert code == 0
    assert "1 of 3 foreign routes cleared by model-endpoints.yaml (openai-codex gpt-6.1-sol)." in out
    assert "not cleared: glm-coding-plan glm-5.3 — the endpoint glm-coding-plan states no data residency" in out
    assert (
        "- Criterion 1 (measured stage-2 runs, ADR 0007): 1 runs measured; rows marked Broke a test `yes` (any status): 0."
        in out
    )
    assert "- Criterion 3 (leak check green in every run): 1 of 1 recorded calls clean;" in out
    assert "Criterion 2 (lakeswitch-ai's disclosure decision): not measured here" in out
    cost = [line for line in out.splitlines() if "oken" in line or "cost" in line]
    assert cost == ["- Tokens and cost per vendor: not recorded by the runner."]


def test_rev_decodes_git_output_as_utf_8_whatever_the_locale(tmp_path: Path, monkeypatch) -> None:
    """Fault: `git show` decoded with the locale's encoding, which garbles non-ASCII text (loop row L1-5)."""
    findings = SIMPLE.replace("# Findings", "# Findings — Prüfung")
    make_repo(tmp_path, {"plans/changes/run": {"findings.md": findings}})
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "one")
    seen: list[str | None] = []
    real = subprocess.run

    def recording(*args, **kwargs):
        seen.append(kwargs.get("encoding"))
        return real(*args, **kwargs)

    monkeypatch.setattr(stage2_runs.subprocess, "run", recording)
    source = stage2_runs.Source(tmp_path, "HEAD")
    assert "Prüfung" in source.read("plans/changes/run/findings.md")
    assert seen and set(seen) == {"utf-8"}


def test_rev_lists_an_archived_folder_name_whole(tmp_path: Path, capsys) -> None:
    """Fault: `git ls-tree` output split on blanks, so `old 2026-10-02-run` yields a second match (loop row L2-1)."""
    make_repo(
        tmp_path,
        {
            "plans/changes/archive/2026-10-01-run": {"findings.md": SIMPLE},
            "plans/changes/archive/old 2026-10-02-run": {"findings.md": SIMPLE},
        },
    )
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "one")
    for rev in ((), ("--rev", "HEAD")):
        code, out, err = run(tmp_path, "run", *rev, capsys=capsys)
        assert code == 0, (rev, err)
        assert "(`plans/changes/archive/2026-10-01-run`)" in table_row(out, "run")[0]


def test_a_findings_file_that_is_not_utf_8_exits_2_without_a_traceback(tmp_path: Path, capsys) -> None:
    """Fault: an invalid byte raising UnicodeDecodeError out of main, in either mode (loop row L2-2)."""
    make_repo(tmp_path, {"plans/changes/run": {"findings.md": SIMPLE}})
    (tmp_path / "plans/changes/run/findings.md").write_bytes(b"# Findings \xff\n")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "one")
    for rev in ((), ("--rev", "HEAD")):
        code, out, err = run(tmp_path, "run", *rev, capsys=capsys)
        assert (code, out) == (2, ""), rev
        assert "is not UTF-8 text" in err, rev


def test_a_yes_counts_in_every_table_that_has_the_column() -> None:
    """Fault: only phase-2a, phase-6 and loop tables of the runner's widths read (phase 6, F-1)."""
    other = stage2.render_table(["ID", "Note", "Broke a test"], [["X-1", "wider or narrower", "yes"]])
    text = (
        HEADER
        + "\n## Follow-up verification\n\n"
        + codex_rows(("F-9", "MINOR", "closed", "yes"))
        + "\n\n"
        + other
        + "\n"
    )
    assert stage2_runs.measure(text).broke == 2


def test_a_call_line_not_in_the_runners_form_stays_in_the_count() -> None:
    """Fault: a line with the call prefix dropped because the rest does not parse (phase 6, F-2)."""
    text = HEADER + "\n" + call("review") + "\n\nStage-2 call, 2026-10-09:review · leak check BLOCK.\n"
    counts = stage2_runs.measure(text)
    assert counts.calls == [("review", True), ("unparsed", False)]


def test_rev_resolves_its_commit_once(tmp_path: Path) -> None:
    """Fault: the label taken from HEAD at one moment and the files read from HEAD later (phase 6, F-3)."""
    make_repo(tmp_path, {"plans/changes/run": {"findings.md": SIMPLE}})
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "one")
    first = _git(tmp_path, "rev-parse", "HEAD")
    source = stage2_runs.Source(tmp_path, "HEAD")
    (tmp_path / "plans/changes/run/findings.md").write_text(SIMPLE + "\n" + call("review") + "\n", encoding="utf-8")
    _git(tmp_path, "commit", "-q", "-am", "two")
    assert source.rev == first
    assert source.label().startswith(f"`{first[:7]}")
    assert source.read("plans/changes/run/findings.md") == SIMPLE


@pytest.mark.parametrize("declaration", ["endpunkte: 42\n", "- a\n- b\n"])
def test_a_declaration_of_the_wrong_shape_is_reported_not_raised(tmp_path: Path, capsys, declaration: str) -> None:
    """Fault: `declaration_problem` raising TypeError or AttributeError out of the counter (phase 6, F-4)."""
    make_repo(tmp_path, {"plans/changes/run": {"findings.md": SIMPLE}}, endpoints=declaration)
    code, out, _ = run(tmp_path, "run", capsys=capsys)
    assert code == 0
    assert "0 of 3 foreign routes cleared" in out
    assert "has a shape the declaration check cannot read" in out


def test_a_header_is_the_line_above_the_separator_and_ends_with_its_table() -> None:
    """Fault: a header known only by a first cell `ID` (F-5), or kept past a heading into the next table (F-6)."""
    no_id = stage2.render_table(["Finding", "Broke a test"], [["X-1", "yes"]])
    assert stage2_runs.measure(HEADER + "\n" + no_id + "\n").broke == 1
    first = stage2.render_table(["ID", "Broke a test"], [["X-1", "no"]])
    second = stage2.render_table(["Name", "Available"], [["example", "yes"]])
    assert stage2_runs.measure(HEADER + "\n" + first + "\n## Availability\n" + second + "\n").broke == 0
    assert stage2_runs.measure(HEADER + "\n" + first + "\nprose\n" + second + "\n").broke == 0


def test_a_body_row_is_a_row_whatever_its_first_cell_or_dashes() -> None:
    """Fault: a body row `ID, yes` taken for a header (F-7), or a body row `---, ---` for a separator (F-8)."""
    id_row = stage2.render_table(["Finding", "Broke a test"], [["ID", "yes"]])
    assert stage2_runs.measure(HEADER + "\n" + id_row + "\n").broke == 1
    dashes = stage2.render_table(["ID", "Broke a test"], [["---", "---"], ["X-1", "yes"]])
    assert stage2_runs.measure(HEADER + "\n" + dashes + "\n").broke == 1
