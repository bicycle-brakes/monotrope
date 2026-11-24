"""The per-model findings report and the shared findings reader (bead coding-harness-qut1).

Criteria 1-8 and 10-19 of plans/changes/findings-per-model/spec.md (criterion 9
is `tests/test_finding_duplicates.py`, criterion 17 is checked in phase 6).
Every tree a test reads is built in `tmp_path`; the one exception is the make
entry point, which reads this checkout's own history. Each test stands next to
the fault that turns it red.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import findings_per_model as fpm  # noqa: E402
import findings_reader as fr  # noqa: E402

RELEASE = "## Phase 4b — loop rows, released 2026-11-01"
RELEASE_2 = "## Phase 4b — loop rows, released 2026-11-02"
GLM_RELEASE = "## Phase 4b — GLM loop rows, released 2026-11-01"
PHASE6 = "## Phase 6 — Codex, 2026-11-01"
PHASE6_2 = "## Phase 6 — Codex, 2026-11-02"
IDENTITY = ["-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false"]


def lrow(row_id: str, reviewer: str, status: str) -> str:
    """A released loop row: ten cells."""
    return f"| {row_id} | MAJOR | CODE | loop | x.py | a finding | {reviewer} | {status} | no | – |"


def p6row(row_id: str, status: str) -> str:
    """A historical phase-6 row: seven cells."""
    return f"| {row_id} | MAJOR | CODE | x.py | a finding | Codex | {status} |"


def call(verb: str, model: str) -> str:
    return f"Stage-2 call, 2026-11-01: {verb} · model {model} · route test · attempt 1"


def doc(*parts: str) -> str:
    return "\n".join(parts) + "\n"


def read(text: str, change: str = "c1", source: fr.AttributionSource | None = None) -> fr.ReaderResult:
    return fr.read_change(change, f"plans/changes/{change}/findings.md", text, source=source)


def totals(findings: list[fr.Finding]) -> dict[str | None, dict]:
    return {record["model"]: record for record in fpm.totals_of(findings)}


# --- git helpers -------------------------------------------------------------------


def git(root: Path, *args: str) -> str:
    command = ["git", "-C", str(root), *IDENTITY, *args]
    return subprocess.run(command, capture_output=True, text=True, check=True).stdout.strip()


def commit(root: Path, files: dict[str, str | bytes]) -> str:
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "step")
    return git(root, "rev-parse", "HEAD")


def repo(tmp_path: Path, files: dict[str, str | bytes]) -> tuple[Path, str]:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q", "-b", "main")
    return root, commit(root, {"plans/changes/archive/.keep": "", **files})


def findings_path(name: str, archived: bool = False) -> str:
    base = "plans/changes/archive/2026-10-01-" if archived else "plans/changes/"
    return f"{base}{name}/findings.md"


def run_report(root: Path, rev: str | None, monkeypatch, state: Path) -> tuple[int, list[str]]:
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    chunks: list[str] = []
    code = fpm.run(root, rev, out=chunks.append)
    return code, chunks


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


# --- criterion 1 ---------------------------------------------------------------------


def test_scope_at_single_commit(tmp_path):
    rejected = doc("## Rejected phase-6 answer, 2026-11-01", p6row("R-1", "fixed"))
    glm1 = lrow("L1-1", "glm-5.3-flash", "fixed")
    glm2 = lrow("L1-2", "glm-5.3-flash", "open")
    alpha1 = doc(RELEASE, glm1, "") + rejected
    alpha2 = doc(RELEASE, glm1, glm2, "") + rejected
    beta = doc(PHASE6, p6row("F-1", "open"))
    root, sha1 = repo(tmp_path, {findings_path("alpha"): alpha1, findings_path("beta", archived=True): beta})
    sha2 = commit(root, {findings_path("alpha"): alpha2})

    first = totals(fpm.collect(root, sha1)[0])
    assert first["glm-5.3-flash"]["raised"] == 1, "the eligible row of the first commit is omitted"
    assert first[None]["raised"] == 1, "the archived change's phase-6 row is omitted"
    assert sum(record["raised"] for record in first.values()) == 2, "a rejected answer was counted"

    second = totals(fpm.collect(root, sha2)[0])
    assert second["glm-5.3-flash"]["raised"] == 2, "the second commit's row is omitted"
    # evidence of another commit is never combined
    assert totals(fpm.collect(root, sha1)[0]) == first
    labels = [table.label for table in fpm.collect(root, sha1)[2]]
    assert "rejected phase-6 answer tables" in labels, "a rejected answer must stand outside the count, visibly"


# --- criterion 2 ---------------------------------------------------------------------


def test_latest_row_per_change_and_id():
    text = doc(
        RELEASE,
        lrow("L1-1", "glm-5.3-flash", "open"),
        "",
        RELEASE_2,
        lrow("L1-1", "gpt-6.1-terra", "fixed — tests/x.py::t"),
    )
    one = read(text, "c1").findings
    assert len(one) == 1
    assert one[0].model == "glm-5.3-flash", "a re-check changed the credited model"
    assert one[0].outcome == "defects_accepted", "an older Status won over the latest one"
    merged = totals(one + read(text, "c2").findings)
    assert merged["glm-5.3-flash"]["raised"] == 2, "the same id in two changes was collapsed"


# --- criterion 3 ---------------------------------------------------------------------


def test_loop_model_attribution():
    named = doc(RELEASE, lrow("L1-1", "hy3", "open"))
    assert read(named).findings[0].model == "hy3", "a named model's row is attributed elsewhere"

    legacy = doc(call("review-loop", "glm-5.3-flash"), "", GLM_RELEASE, lrow("L1-1", "GLM", "open"))
    assert read(legacy).findings[0].model == "glm-5.3-flash", "GLM was not resolved through the call line"

    no_call = doc(GLM_RELEASE, lrow("L1-1", "GLM", "open"))
    assert read(no_call).findings[0].model is None, "a vendor-only row without a call line must be unattributed"


def test_vendor_qualified_loop_model_is_attributed():
    result = read(doc(RELEASE, lrow("L1-1", "Vendor/model-free", "fixed")))
    assert not result.gaps
    assert result.findings[0].model == "Vendor/model-free"
    assert totals(result.findings)["Vendor/model-free"]["defects_accepted"] == 1


def test_digitless_free_swarm_model_is_attributed():
    """Released loop rows from digitless free-swarm model IDs credit that model (RF6-1)."""
    text = doc(RELEASE, lrow("L1-1", "space-bunny-free", "open"), lrow("L1-2", "big-pickle", "fixed"))
    models = {finding.id: finding.model for finding in read(text).findings}
    assert models == {"L1-1": "space-bunny-free", "L1-2": "big-pickle"}
    vendor = doc(RELEASE, lrow("L1-3", "Codex", "open"), lrow("L1-4", "reviewer", "open"))
    assert [finding.model for finding in read(vendor).findings] == [None, "reviewer"]


# --- criterion 4 ---------------------------------------------------------------------


def test_phase6_nearest_call_boundary():
    review = call("review", "gpt-6.1-terra")
    row1 = p6row("F-1", "open")
    direct = doc(review, "", PHASE6, row1)
    assert read(direct).findings[0].model == "gpt-6.1-terra"

    repaired = doc(review, call("repair", "gpt-6.1-terra"), "", PHASE6, row1)
    assert read(repaired).findings[0].model is None, "a repair call was skipped to reach an older review call"

    looped = doc(review, call("review-loop", "hy3"), "", PHASE6, row1)
    assert read(looped).findings[0].model is None, "a review-loop call was used or skipped"

    between = doc(review, "", PHASE6, row1, "", PHASE6_2, p6row("F-2", "open"))
    found = {finding.id: finding.model for finding in read(between).findings}
    assert found == {"F-1": "gpt-6.1-terra", "F-2": None}, "a call across another phase-6 block was used"


# --- criterion 5 ---------------------------------------------------------------------


def test_unattributed_rows_are_visible():
    result = read(doc(PHASE6, p6row("F-1", "fixed")), "c1")
    assert [(finding.change, finding.id, finding.model) for finding in result.findings] == [("c1", "F-1", None)]
    assert totals(result.findings)[None]["raised"] == 1, "the unpaired seven-cell row disappeared"
    records = fpm.jsonl_records("a" * 40, True, fpm.totals_of(result.findings), result.findings, [])
    assert {"type": "finding", "change": "c1", "id": "F-1"} in records


def test_unattributed_table_lists_change_and_id(tmp_path, monkeypatch):
    root, _ = repo(tmp_path, {findings_path("c1"): doc(PHASE6, p6row("F-1", "fixed"))})
    code, chunks = run_report(root, None, monkeypatch, tmp_path / "state")
    output = "".join(chunks)
    records = jsonl(Path(chunks[-1].strip()))
    assert code == 0
    assert {"type": "finding", "change": "plans/changes/c1", "id": "F-1"} in records
    assert "- plans/changes/c1: F-1" in output.split("| unattributed |", 1)[1]


# --- criterion 6 ---------------------------------------------------------------------


class HeadingOnly(fr.AttributionSource):
    """A substitute source that attributes from the heading alone."""

    def __init__(self) -> None:
        self.seen: list[fr.BlockIdentity] = []

    def attribute(self, block: fr.BlockIdentity) -> str:
        self.seen.append(block)
        return "hy3" if block.heading and block.heading.startswith("## Phase 6") else fr.UNATTRIBUTED


def test_replace_attribution_source(tmp_path):
    text = doc(PHASE6, p6row("F-1", "open"))
    assert read(text).findings[0].model is None
    source = HeadingOnly()
    assert read(text, source=source).findings[0].model == "hy3", "the replacement source did not attribute"
    identity = source.seen[0]
    assert identity.change == "c1" and identity.findings_file.endswith("findings.md")
    assert identity.heading == PHASE6 and identity.position == 1 and identity.preceding_calls == ()

    # the report consumer passes the source on; its reader call keeps its shape
    root, sha = repo(tmp_path, {findings_path("c1"): text})
    assert totals(fpm.collect(root, sha, source=HeadingOnly())[0])["hy3"]["raised"] == 1


# --- criteria 7 and 8 ----------------------------------------------------------------


@pytest.mark.parametrize(
    "status",
    [
        "rejected — Same as L1-1",
        "Duplicate of L2-2",
        "rejected — repeat of F-3",
        "REPEATS L1-1",
        "repeat L1-1",
        "rejected — duplicate of L1-1 and L1-2: same shell",
    ],
)
def test_legacy_duplicate_markers(status):
    assert fr.is_duplicate(status), f"a valid duplicate marker was missed: {status!r}"
    assert fr.duplicate_targets(status)


@pytest.mark.parametrize(
    "status",
    ["rejected — same as above", "rejected — a repeat", "repeats finding 3", "fixed", "open", "rejected — duplicates"],
)
def test_legacy_duplicate_markers_without_id(status):
    assert not fr.is_duplicate(status), f"a marker without a row id counted as a duplicate: {status!r}"


def test_duplicate_credits_each_named_original():
    text = doc(
        RELEASE,
        lrow("L1-1", "glm-5.3-flash", "fixed"),
        lrow("L1-2", "hy3", "rejected — duplicate of L1-1"),
        lrow("L1-3", "hy3", "rejected — same as L1-2"),
        lrow("L1-4", "hy3", "rejected — duplicate of L1-1 and L1-3"),
    )
    result = read(text)
    assert result.gaps == []
    by_model = totals(result.findings)
    assert by_model["glm-5.3-flash"]["raised"] == 1 and by_model["glm-5.3-flash"]["defects_accepted"] == 1
    assert "hy3" not in by_model, "a duplicate earned credit"

    unattributed_root = doc(
        PHASE6,
        p6row("F-1", "fixed"),
        "",
        RELEASE,
        lrow("L1-1", "glm-5.3-flash", "rejected — duplicate of F-1"),
    )
    by_model = totals(read(unattributed_root).findings)
    assert by_model[None]["raised"] == 1 and by_model[None]["defects_accepted"] == 1, "the root lost its credit"
    assert "glm-5.3-flash" not in by_model, "an unattributed root's credit moved to a duplicate's model"


def test_jsonl_excludes_unattributed_duplicates():
    result = read(doc(PHASE6, p6row("F-1", "fixed"), p6row("F-2", "rejected — duplicate of F-1")))
    assert not result.gaps
    records = fpm.jsonl_records("a" * 40, True, fpm.totals_of(result.findings), result.findings, result.gaps)
    assert [record for record in records if record["type"] == "finding"] == [
        {"type": "finding", "change": "c1", "id": "F-1"}
    ], "only the unattributed root should be listed"


# --- criteria 10-13 ------------------------------------------------------------------


def test_raised_counts_open_and_rejected_once():
    text = doc(
        RELEASE,
        lrow("L1-1", "hy3", "open"),
        lrow("L1-2", "hy3", "rejected — wrong"),
        lrow("L1-3", "hy3", "fixed"),
        "",
        RELEASE_2,
        lrow("L1-3", "hy3", "fixed — again"),
    )
    assert totals(read(text).findings)["hy3"]["raised"] == 3, "an open finding was omitted or one counted twice"


def test_defects_accepted_statuses():
    text = doc(
        RELEASE,
        lrow("L1-1", "hy3", "taken"),
        lrow("L1-2", "hy3", "fixed — orchestrator hand edit"),
        lrow("L1-3", "hy3", "closed — merged in #12"),
        lrow("L1-4", "hy3", "rejected — wrong"),
    )
    record = totals(read(text).findings)["hy3"]
    assert record["defects_accepted"] == 3, "fixed or historical closed was omitted, or a rejection included"
    assert record["rejected"] == 1


def test_questions_settled_statuses():
    text = doc(
        RELEASE,
        lrow("L1-1", "hy3", "resolved 2026-11-18 by decisions.md"),
        lrow("L1-2", "hy3", "answered"),
        lrow("L1-3", "hy3", "in spec"),
        lrow("L1-4", "hy3", "taken"),
    )
    record = totals(read(text).findings)["hy3"]
    assert record["questions_settled"] == 3, "a resolved question was omitted or a taken defect included"
    assert record["defects_accepted"] == 1


def test_rejected_status():
    text = doc(RELEASE, lrow("L1-1", "hy3", "rejected — not a bug"), lrow("L1-2", "hy3", "open"))
    record = totals(read(text).findings)["hy3"]
    assert record["rejected"] == 1
    assert record["raised"] == 2
    assert record["defects_accepted"] == 0 and record["questions_settled"] == 0, "an open row got an outcome"


# --- criterion 14 --------------------------------------------------------------------


def test_formats_agree_and_name_commit(tmp_path, monkeypatch):
    text = doc(
        RELEASE,
        lrow("L1-1", "glm-5.3-flash", "fixed"),
        lrow("L1-2", "hy3", "rejected — wrong"),
        lrow("L1-3", "hy3", "resolved 2026-11-18"),
        "",
        PHASE6,
        p6row("F-1", "open"),
    )
    root, sha = repo(tmp_path, {findings_path("c1"): text})
    state = tmp_path / "state"
    base = state / "coding-harness" / "findings-per-model"

    try:
        code, chunks = run_report(root, None, monkeypatch, state)
    except NotADirectoryError:
        pytest.fail("an unwritable state path must produce an incomplete report")
    assert code == 0
    output = "".join(chunks)
    main_file = base / "main.jsonl"
    assert main_file.exists()
    assert chunks[-1].strip() == str(main_file), "the file path is not printed last"
    assert sha in output.splitlines()[0], "the table does not name the full cutoff commit"

    records = jsonl(main_file)
    assert records[0] == {"type": "metadata", "commit": sha, "complete": True}
    models = [record for record in records if record["type"] == "model"]
    assert [record["model"] for record in models] == ["glm-5.3-flash", "hy3", None]
    for record in models:
        label = "unattributed" if record["model"] is None else record["model"]
        counts = [record[key] for key in ("raised", "defects_accepted", "questions_settled", "rejected")]
        expected = f"| {label} | " + " | ".join(str(count) for count in counts) + " |"
        assert expected in output, f"the table and the JSON Lines disagree for {label}"
    assert {"type": "finding", "change": "plans/changes/c1", "id": "F-1"} in records

    # a branch has its own file and never overwrites main
    before = main_file.read_text(encoding="utf-8")
    git(root, "checkout", "-q", "-b", "feat/x")
    commit(root, {findings_path("c2"): doc(RELEASE, lrow("L1-1", "hy3", "open"))})
    code, chunks = run_report(root, None, monkeypatch, state)
    branch_file = base / "branches" / (b"feat/x".hex() + ".jsonl")
    assert code == 0 and branch_file.exists()
    assert chunks[-1].strip() == str(branch_file)
    assert main_file.read_text(encoding="utf-8") == before, "a branch output overwrote main"

    # a revision that is no branch tip writes revisions/<full commit>.jsonl
    revision_file = base / "revisions" / f"{sha}.jsonl"
    code, chunks = run_report(root, sha, monkeypatch, state)
    assert revision_file.exists()
    assert chunks[-1].strip() == str(revision_file)


def test_origin_main_writes_main_report(tmp_path, monkeypatch):
    root, sha = repo(tmp_path, {findings_path("c1"): doc(RELEASE, lrow("L1-1", "hy3", "open"))})
    git(root, "update-ref", "refs/remotes/origin/main", sha)
    git(root, "checkout", "-q", "-b", "feature")
    commit(root, {findings_path("c2"): doc(RELEASE, lrow("L1-2", "hy3", "fixed"))})
    state = tmp_path / "state"
    code, chunks = run_report(root, "origin/main", monkeypatch, state)
    output = state / "coding-harness/findings-per-model/main.jsonl"
    assert code == 0
    assert chunks[-1].strip() == str(output)
    assert jsonl(output)[0]["commit"] == sha


# --- criterion 15 --------------------------------------------------------------------


def test_make_entry_point_and_revision(tmp_path):
    lookup = ["git", "-C", str(REPO_ROOT), "rev-parse", "--verify", "HEAD~1^{commit}"]
    probe = subprocess.run(lookup, capture_output=True, text=True, check=False)
    if probe.returncode != 0:
        pytest.skip("HEAD~1 is not available in this checkout")
    expected = probe.stdout.strip()
    env = {**os.environ, "XDG_STATE_HOME": str(tmp_path / "state")}
    env.pop("REV", None)
    # the Makefile calls `python3` from PATH: put the interpreter running this test first
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    command = ["make", "-C", str(REPO_ROOT), "findings-per-model", "REV=HEAD~1"]
    done = subprocess.run(command, capture_output=True, text=True, check=False, env=env)
    # the exit code may be non-zero on real history: gaps are reported, never hidden
    assert done.stdout.strip(), f"the report printed nothing: stderr {done.stderr[:600]!r}"
    lines = done.stdout.splitlines()
    assert expected in lines[0], f"the requested revision was ignored: {done.stdout[:300]!r} {done.stderr[:300]!r}"
    wanted = tmp_path / "state" / "coding-harness" / "findings-per-model" / "revisions" / f"{expected}.jsonl"
    assert Path(lines[-1].strip()) == wanted, "the JSON Lines file is missing or its path is not printed last"
    assert jsonl(wanted)[0]["commit"] == expected
    assert "| Model |" in done.stdout, "the table is missing"


# --- criterion 16 --------------------------------------------------------------------


def test_gaps_produce_both_incomplete_outputs_and_nonzero(tmp_path, monkeypatch):
    bad = doc(
        RELEASE,
        lrow("L1-1", "hy3", "maybe later"),
        lrow("L1-2", "hy3", "rejected — same as L9-9"),
        lrow("L1-3", "hy3", "duplicate of L1-4"),
        lrow("L1-4", "hy3", "duplicate of L1-3"),
        "| L1-5 | MAJOR | too few cells |",
    )
    files = {findings_path("bad"): bad, findings_path("raw"): b"\xff\xfe not utf-8"}
    root, _ = repo(tmp_path, files)
    state = tmp_path / "state"
    code, chunks = run_report(root, None, monkeypatch, state)
    assert code != 0, "a report with gaps exited zero"
    output = "".join(chunks)
    assert "Incomplete" in output
    needles = ("maybe later", "L9-9", "duplicate cycle", "UTF-8", "L1-5")
    for needle in needles:
        assert needle in output, f"the gap {needle!r} is not shown in the table output"
    records = jsonl(state / "coding-harness" / "findings-per-model" / "main.jsonl")
    assert records[0]["complete"] is False
    reasons = " ".join(record["reason"] for record in records if record["type"] == "gap")
    for needle in needles[:4]:
        assert needle in reasons, f"the gap {needle!r} is missing from the JSON Lines"

    # accepted limit is a known status: raised only, no gap
    result = read(doc(RELEASE, lrow("L1-1", "hy3", "accepted limit — style")))
    assert result.gaps == []
    record = totals(result.findings)["hy3"]
    assert record["raised"] == 1 and record["defects_accepted"] == 0, "accepted limit was counted as fixed"


def test_malformed_finding_cells_are_gaps_in_both_outputs(tmp_path, monkeypatch):
    # Maintainer decision 2026-11-20 ("the reader measures, the gate enforces"): blank cells are gaps, free vocabulary is not.
    valid = ["F-1", "MAJOR", "SPEC", "base", "spec.md", "a finding", "open"]
    rows = []
    for index, value in enumerate(("bad id", "", "", "", "", "", "unknown")):
        cells = valid.copy()
        cells[index] = value
        if index != 0:
            cells[0] = f"F-{index + 1}"
        rows.append("| " + " | ".join(cells) + " |")
    rows.append("| F-8 | | | | | | open |")
    root, _ = repo(tmp_path, {findings_path("bad-cells"): doc(PHASE6, *rows)})
    state = tmp_path / "state"
    code, chunks = run_report(root, None, monkeypatch, state)
    records = jsonl(state / "coding-harness" / "findings-per-model" / "main.jsonl")
    assert code != 0 and "Incomplete" in "".join(chunks)
    assert records[0]["complete"] is False
    assert len([record for record in records if record["type"] == "gap"]) == len(rows)
    assert not [record for record in records if record["type"] == "model"]


@pytest.mark.parametrize(
    "row",
    [
        "| L2-1 | MINOR | MAINT | impl | x.py | a finding | hy3 | fixed — tests/x.py::t | no | – |",
        "| L1-1 | MAJOR | Correctness | base | x.py | a finding | hy3 | open | no | – |",
        "| L1-11 | MAINT | MAINT | change | x.py | a finding | hy3 | rejected — style | no | – |",
    ],
    ids=["origin-impl", "free-dimension", "free-severity"],
)
def test_historic_free_vocabulary_rows_are_counted(row):
    # Maintainer decision 2026-11-20 ("the reader measures, the gate enforces"): a historic row with `impl` counts.
    result = read(doc(RELEASE, row))
    assert result.gaps == [], "a free origin, severity or dimension made the report incomplete"
    assert [(finding.model, finding.id) for finding in result.findings] == [("hy3", row.split(" | ")[0][2:])]
    assert totals(result.findings)["hy3"]["raised"] == 1


# --- criterion 18 --------------------------------------------------------------------


def test_headingless_tables_outside_count():
    text = doc(
        p6row("H-1", "fixed"),
        "",
        "## Phase 2a — spec review, 2026-11-01",
        p6row("2a-1", "answered"),
        "",
        "## Phase 2a — spec review, round 2",
        p6row("2a-2", "answered"),
        "",
        RELEASE,
        lrow("L1-1", "hy3", "open"),
        "",
        "## Restated for the reader",
        lrow("L1-1", "hy3", "fixed"),
    )
    result = read(text)
    labels = {table.label: table.rows for table in result.outside}
    assert labels["headingless tables"] == 1, "a table before any heading was omitted"
    assert labels["phase-2a tables"] == 2, "phase-2a blocks are not grouped"
    assert labels["## Restated for the reader"] == 1
    assert [finding.id for finding in result.findings] == ["L1-1"], "an outside table was credited"
    assert result.findings[0].status == "open", "a restatement changed an eligible row's Status"
    assert result.findings[0].outcome is None


# --- criterion 19 --------------------------------------------------------------------


def test_phase2a_ids_excluded():
    result = read(doc(PHASE6, p6row("2a-1", "answered"), p6row("F-1", "fixed")))
    assert [finding.id for finding in result.findings] == ["F-1"]
    assert totals(result.findings)[None]["raised"] == 1, "a 2a row increased a total"
    assert result.gaps == []


# --- the mirror of the runner's row shapes -----------------------------------------


def test_row_shapes_match_the_runner():
    stage2 = (REPO_ROOT / "scripts" / "stage2.py").read_text(encoding="utf-8")
    assert f'RELEASE_HEADING = "{fr.RELEASE_HEADING}"' in stage2, "the release heading drifted from the writer"
    import stage2 as writer

    assert fr.ROW_COLUMNS == writer.ROW_COLUMNS
    assert fr.RELEASED_COLUMNS == writer.RELEASED_COLUMNS
    line = writer.call_line("review", ("test", "glm-5.3", None), SimpleNamespace(files=1, commits=2, rules=3))
    parsed = fr.parse_call_line(line, 1)
    assert parsed is not None and parsed.verb == "review" and parsed.model == "glm-5.3"


def test_duplicate_reason_does_not_add_targets():
    status = "rejected — duplicate of L1-1: see L1-2"
    assert fr.duplicate_targets(status) == ["L1-1"], "reason IDs are not duplicate targets"
    result = read(doc(RELEASE, lrow("L1-1", "hy3", "fixed"), lrow("L1-3", "hy3", status)))
    assert not result.gaps, "a reason ID must not create a missing-target gap"


def test_canonical_duplicate_reason_marker_does_not_add_targets():
    status = "rejected — duplicate of L1-1: not the same as L1-3"
    assert fr.duplicate_targets(status) == ["L1-1"]
    result = read(doc(RELEASE, lrow("L1-1", "hy3", "fixed"), lrow("L1-3", "hy3", status)))
    assert not result.gaps, "a marker in the reason must not create a cycle"


def test_statuses_require_whole_leading_words():
    for status in ("fixedy", "rejectedly", "openly", "takenish", "in specialty"):
        assert not fr.known_status(status), f"malformed status accepted: {status}"
        assert fr.status_outcome(status) is None, f"malformed status counted: {status}"


def test_duplicate_marker_targets_are_anchored_after_colon():
    assert fr.duplicate_targets("rejected 2026-11-18 — false: repeat of L1-6 and L3-3; see L9-9") == ["L1-6", "L3-3"]
    assert fr.duplicate_targets("fixed — hand edit: same as L4-4") == ["L4-4"]
    assert not fr.is_duplicate("rejected L1-1 — same as above")
    assert not fr.is_duplicate("rejected — same as 2026-11-18")


def test_legacy_release_calls_cross_phase6_but_not_previous_release():
    text = doc(
        call("review-loop", "glm-5.3"),
        PHASE6,
        p6row("F-1", "open"),
        GLM_RELEASE,
        lrow("L1-1", "GLM", "open"),
        RELEASE_2,
        lrow("L2-1", "GLM", "open"),
    )
    found = {f.id: f.model for f in read(text).findings}
    assert found["L1-1"] == "glm-5.3"
    assert found["L2-1"] is None


def test_legacy_loop_vendor_matches_unique_review_loop_model():
    def model(*calls: str, reviewer: str = "GLM") -> str | None:
        text = doc(*calls, PHASE6, p6row("F-1", "open"), GLM_RELEASE, lrow("L1-1", reviewer, "open"))
        return next(f.model for f in read(text).findings if f.id == "L1-1")

    loop = call("review-loop", "glm-5.3")
    review = call("review", "gpt-6.1-sol")
    assert model(loop, review) == "glm-5.3"
    assert model(loop, loop, review) == "glm-5.3"
    assert model(loop, call("review-loop", "glm-5.3-flash"), review) is None
    assert model(call("review-loop", "gpt-6.1-sol"), review) is None
    assert model(call("repair", "glm-5.3"), review) is None
    assert model(loop, review, reviewer="Other") == "Other"


def test_historical_statuses_require_dash():
    for status in ("closed", "accepted limit"):
        assert not fr.known_status(status)
        assert fr.status_outcome(status) is None
    assert fr.known_status("closed — merged")
    assert fr.known_status("accepted limit — documented")


def test_detached_main_tip_uses_revision_output(tmp_path):
    root, sha = repo(tmp_path, {"a": "one"})
    git(root, "checkout", "--detach", "-q")
    assert fpm.output_relative(root, None, sha) == f"revisions/{sha}.jsonl"
    git(root, "checkout", "-q", "-b", "other")
    later = commit(root, {"a": "two"})
    git(root, "checkout", "--detach", "-q")
    assert fpm.output_relative(root, None, later) == f"revisions/{later}.jsonl"


def test_explicit_head_uses_default_output(tmp_path, monkeypatch):
    root, main_sha = repo(tmp_path, {findings_path("c1"): doc(RELEASE, lrow("L1-1", "hy3", "open"))})
    state = tmp_path / "state"
    for expected in ("main.jsonl", f"branches/{b'feature/x'.hex()}.jsonl"):
        _, default = run_report(root, None, monkeypatch, state)
        _, explicit = run_report(root, "HEAD", monkeypatch, state)
        assert default[-1] == explicit[-1]
        assert explicit[-1].strip().endswith(expected)
        if expected == "main.jsonl":
            git(root, "checkout", "-q", "-b", "feature/x")
            commit(root, {"a": "later"})
    _, historical = run_report(root, main_sha, monkeypatch, state)
    assert historical[-1].strip().endswith(f"revisions/{main_sha}.jsonl")


def test_subheading_restated_phase6_rows_are_outside():
    result = read(doc(PHASE6, p6row("F-1", "open"), "### Restatement", p6row("F-1", "fixed")))
    assert result.findings[0].status == "open"
    assert [(table.label, table.rows) for table in result.outside] == [("### Restatement", 1)]


def test_calls_in_reviewer_prose_do_not_change_attribution():
    text = doc(
        call("review", "original-model"),
        "### Reviewer prose",
        "> " + call("review", "stray-model"),
        PHASE6,
        p6row("F-1", "open"),
    )
    result = read(text)
    assert next(f.model for f in result.findings if f.id == "F-1") == "original-model"


def test_calls_after_kept_block_and_subheadings_are_attributed():
    text = doc(
        RELEASE,
        lrow("L1-1", "hy3", "open"),
        "Kept from the loop record:",
        "",
        "> " + call("review", "stray-model"),
        "",
        call("review", "gpt-6.1-sol"),
        PHASE6,
        p6row("F-1", "open"),
        "### Details",
        "> quoted prose",
        "",
        call("review", "gpt-6.1-terra"),
        PHASE6_2,
        p6row("F-2", "open"),
    )
    models = {f.id: f.model for f in read(text).findings}
    assert models["F-1"] == "gpt-6.1-sol"
    assert models["F-2"] == "gpt-6.1-terra"


def test_outside_tables_identify_their_source(tmp_path, monkeypatch):
    root, _ = repo(
        tmp_path,
        {
            findings_path("a"): doc("## Phase 2a", p6row("F-1", "open")),
            findings_path("b"): doc("## Phase 2a", p6row("F-2", "open")),
        },
    )
    code, chunks = run_report(root, None, monkeypatch, tmp_path / "state")
    output = "".join(chunks)
    assert code == 0
    assert findings_path("a") in output and findings_path("b") in output


def test_failed_git_show_is_an_incomplete_input(tmp_path, monkeypatch):
    path = findings_path("a")
    root, sha = repo(tmp_path, {path: doc(PHASE6, p6row("F-1", "open"))})
    original = fpm.git

    def failing(root, *args):
        if args[0] == "show":
            return SimpleNamespace(returncode=1, stdout=b"", stderr=b"failure")
        return original(root, *args)

    monkeypatch.setattr(fpm, "git", failing)
    code, chunks = run_report(root, sha, monkeypatch, tmp_path / "state")
    assert code == 1 and path in "".join(chunks) and "Incomplete" in "".join(chunks)
    records = jsonl(Path(chunks[-1].strip()))
    assert not records[0]["complete"] and any(r["type"] == "gap" and r["path"] == path for r in records)


def test_unwritable_state_path_reports_gap(tmp_path, monkeypatch):
    root, _ = repo(tmp_path, {findings_path("a"): doc(PHASE6, p6row("F-1", "open"))})
    state = tmp_path / "file"
    state.write_text("not a directory")
    try:
        code, chunks = run_report(root, None, monkeypatch, state)
    except OSError as exc:
        pytest.fail(f"an unwritable state path must end in the report's own gap wording, not raise {exc!r}")
    assert code == 1 and "Incomplete" in "".join(chunks) and "cannot write report" in "".join(chunks)


def test_later_phase6_blocks_after_kept_block_keep_their_own_calls():
    """The shape of a released block with a kept-from record before several phase-6 blocks."""
    text = doc(
        "## Phase 4b — loop rows, released 2026-11-01",
        lrow("L1-1", "hy3", "open"),
        "",
        "Kept from the loop record:",
        "",
        "### Reviewer prose",
        "> quoted prose",
        "",
        call("review", "gpt-6.1-sol"),
        PHASE6,
        p6row("F-1", "open"),
        "",
        call("review", "gpt-6.1-terra"),
        "## Phase 6 — Codex, 2026-11-03",
        p6row("F-2", "open"),
        "",
        call("review", "gpt-6.1-luna"),
        "## Phase 6 — Codex, 2026-11-04",
        p6row("F-3", "open"),
    )
    models = {f.id: f.model for f in read(text).findings}
    assert models == {
        "L1-1": "hy3",
        "F-1": "gpt-6.1-sol",
        "F-2": "gpt-6.1-terra",
        "F-3": "gpt-6.1-luna",
    }


def test_released_section_ends_after_first_table():
    result = read(doc(GLM_RELEASE, lrow("L1-1", "GLM", "open"), "", "Reviewer prose", lrow("L1-2", "GLM", "fixed")))
    assert [finding.id for finding in result.findings] == ["L1-1"]
    assert [(table.label, table.rows) for table in result.outside] == [(GLM_RELEASE, 1)]


def test_unknown_status_with_duplicate_marker_is_gap():
    result = read(doc(PHASE6, p6row("F-1", "open"), p6row("F-2", "nonsense — duplicate of F-1")))
    assert any(gap.id == "F-2" and "unknown status" in gap.reason for gap in result.gaps)


@pytest.mark.parametrize("base", ["plans/changes", "plans/changes/archive"])
def test_failed_change_listing_marks_outputs_incomplete(tmp_path, monkeypatch, base):
    root, _ = repo(
        tmp_path,
        {
            findings_path("a"): doc(PHASE6, p6row("F-1", "open")),
            findings_path("b", archived=True): doc(PHASE6, p6row("F-2", "open")),
        },
    )
    original = fpm.git

    def fail_listing(root, *args):
        if args[:4] == ("ls-tree", "-d", "-z", "--name-only") and args[4].endswith(":" + base):
            return SimpleNamespace(returncode=1, stdout=b"", stderr=b"failure")
        return original(root, *args)

    monkeypatch.setattr(fpm, "git", fail_listing)
    state = tmp_path / "state"
    code, output = run_report(root, None, monkeypatch, state)
    assert code != 0 and "Incomplete" in "".join(output) and base in "".join(output)
    records = jsonl(state / "coding-harness" / "findings-per-model" / "main.jsonl")
    assert not records[0]["complete"]
    assert any(record.get("path") == base for record in records if record["type"] == "gap")


def test_release_heading_requires_exact_date():
    headings = [
        "## Phase 4b — loop rows, released draft",
        "## Phase 4b — GLM loop rows, released 2026-11-01 draft",
        "## Phase 4b — loop rows, released 2026-11-01",
    ]
    result = read(
        doc(*(part for i, heading in enumerate(headings) for part in (heading, lrow(f"L1-{i + 1}", "hy3", "open"))))
    )
    assert [finding.id for finding in result.findings] == ["L1-3"]
    assert {table.label for table in result.outside} == set(headings[:2])


def test_phase6_unreadable_ids_make_report_incomplete(tmp_path, monkeypatch):
    path = findings_path("bad-id")
    root, _ = repo(tmp_path, {path: doc(PHASE6, p6row("", "open"), p6row("???", "fixed"))})
    state = tmp_path / "state"
    code, chunks = run_report(root, None, monkeypatch, state)
    records = jsonl(state / "coding-harness" / "findings-per-model" / "main.jsonl")
    assert code != 0 and "Incomplete" in "".join(chunks)
    assert records[0]["complete"] is False
    gaps = [record for record in records if record["type"] == "gap"]
    assert len(gaps) == 2 and all(record["path"] == path for record in gaps)
    assert all("id" in record["reason"].lower() for record in gaps)
    assert not any(record["type"] == "model" and record["raised"] for record in records)


def test_readable_ids_are_duplicate_targets_and_gate_uses_same_grammar():
    import check_finding_duplicates as gate

    result = read(doc(PHASE6, p6row("R1", "fixed"), p6row("R2", "rejected — same as R1")))
    assert not result.gaps
    assert fr.duplicate_targets("rejected — same as R1") == ["R1"]
    assert sum(item["raised"] for item in fpm.totals_of(result.findings)) == 1
    assert gate.marks_duplicate("rejected — same as R1")
    assert not gate.CANONICAL.fullmatch("rejected — same as R1")
    assert gate.CANONICAL.fullmatch("rejected — duplicate of R1 and L2-5")


def test_incomplete_table_lines_make_report_incomplete(tmp_path, monkeypatch):
    path = findings_path("missing-pipe")
    root, _ = repo(tmp_path, {path: doc(PHASE6, p6row("F-3", "open")[:-1])})
    state = tmp_path / "state"
    code, chunks = run_report(root, None, monkeypatch, state)
    records = jsonl(state / "coding-harness" / "findings-per-model" / "main.jsonl")
    assert code != 0 and "Incomplete" in "".join(chunks)
    assert records[0]["complete"] is False
    assert any(r.get("id") == "F-3" and r.get("path") == path for r in records if r["type"] == "gap")
    parsed = read(doc(RELEASE, lrow("L1-1", "hy3", "open"), lrow("L1-2", "hy3", "open")[:-1]))
    assert any(g.id == "L1-2" for g in parsed.gaps)


def test_deep_duplicate_chain_and_cycle_resolve_without_recursion_error(tmp_path, monkeypatch):
    """F6-2: a 1,200-node duplicate chain and a 1,200-node cycle resolve iteratively without RecursionError."""
    depth = 1200
    chain_rows = [lrow(f"L1-{i:04d}", "hy3", f"rejected — duplicate of L1-{i + 1:04d}") for i in range(1, depth + 1)]
    chain_rows.append(lrow(f"L1-{depth + 1:04d}", "glm-5.3-flash", "fixed"))
    chain_dir = tmp_path / "chain"
    chain_dir.mkdir()
    root, sha = repo(chain_dir, {findings_path("deep"): doc(RELEASE, *chain_rows)})
    state = tmp_path / "state-chain"
    code, chunks = run_report(root, None, monkeypatch, state)
    assert code == 0, "a valid 1,200-node duplicate chain failed to complete"
    output = "".join(chunks)
    assert "| glm-5.3-flash | 1 | 1 | 0 | 0 |" in output
    assert "| hy3 |" not in output
    records = jsonl(Path(chunks[-1].strip()))
    assert records[0] == {"type": "metadata", "commit": sha, "complete": True}
    models = [record for record in records if record["type"] == "model"]
    assert models == [
        {
            "type": "model",
            "model": "glm-5.3-flash",
            "raised": 1,
            "defects_accepted": 1,
            "questions_settled": 0,
            "rejected": 0,
        }
    ]

    cycle_rows = [
        lrow(f"L1-{i:04d}", "hy3", f"rejected — duplicate of L1-{(i % depth) + 1:04d}") for i in range(1, depth + 1)
    ]
    cycle_dir = tmp_path / "cycle"
    cycle_dir.mkdir()
    cycle_root, _ = repo(cycle_dir, {findings_path("deep-cycle"): doc(RELEASE, *cycle_rows)})
    cycle_state = tmp_path / "state-cycle"
    cycle_code, cycle_chunks = run_report(cycle_root, None, monkeypatch, cycle_state)
    assert cycle_code != 0
    assert "duplicate cycle" in "".join(cycle_chunks)
    cycle_records = jsonl(Path(cycle_chunks[-1].strip()))
    assert cycle_records[0]["complete"] is False
    assert any(r["type"] == "gap" and "duplicate cycle" in r["reason"] for r in cycle_records)


def test_plain_model_ids_and_legacy_vendors():
    text = doc(RELEASE, lrow("L1-1", "mercury", "open"), lrow("L1-2", "GLM", "open"))
    result = read(text)
    assert not result.gaps
    assert [f.model for f in result.findings] == ["mercury", None]


def test_symbolic_remote_branch_reports(tmp_path, monkeypatch):
    root, sha = repo(tmp_path, {findings_path("c1"): doc(RELEASE, lrow("L1-1", "hy3", "open"))})
    git(root, "update-ref", "refs/remotes/origin/feat/findings-per-model", sha)
    state = tmp_path / "state"
    expected = state / "coding-harness/findings-per-model/branches" / (b"feat/findings-per-model".hex() + ".jsonl")
    for rev in ("origin/feat/findings-per-model", "refs/remotes/origin/feat/findings-per-model"):
        code, chunks = run_report(root, rev, monkeypatch, state)
        assert code == 0
        assert chunks[-1].strip() == str(expected)
        assert jsonl(expected)[0]["commit"] == sha
