"""Active model-written research has truthful, complete publication metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PLANS = REPO_ROOT / "plans" / "changes"
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2  # noqa: E402

# Research files written before explore published truthful metadata (cut-off: the second merge of origin/main
# into fix/explore-provenance, 2026-11-09 evening). The maintainer decided to ship without correcting them
# (plans/changes/explore-provenance/decisions.md, Q-4); their correction is its own change (bead
# coding-harness-2i7x). The list only shrinks: a corrected or archived file must leave it.
UNCORRECTED = frozenset(
    f"plans/changes/{name}/research.md"
    for name in (
        "address-drift-warning",
        "adr-0016-docs-check",
        "adr-repair-check",
        "archive-closed-changes",
        "docs-job-report-header",
        "night-heartbeat",
        "night-machine-facts",
        "outcome-test",
        "pi-no-compaction",
        "raising-fault-test",
        "red-first-own-refs",
        "redraft-after-scope",
        "repair-targeted-check",
        "review-loop-deep-a",
        "status-fields-restore",
        "swarm-test-speed",
        "time-records-data",
    )
)


def active_research_files() -> list[Path]:
    archive = PLANS / "archive"
    return sorted(path for path in PLANS.glob("*/research.md") if archive not in path.parents)


def census_findings() -> list[str]:
    """Every census finding over active research, before applying legacy exemptions."""
    import research_census as census

    try:
        return census.census_findings(active_research_files(), REPO_ROOT)
    except AttributeError as error:
        pytest.fail(f"The read-only census library must report current research defects: {error}")


def assert_active_model_research_has_no_false_human_provenance(exempt: frozenset[str] = frozenset()) -> None:
    affected = [finding for finding in census_findings() if finding.split(": ", 1)[0] not in exempt]
    assert affected == [], (
        f"active research has unreadable files, false provenance or opening skeleton notices: {affected}"
    )


@pytest.mark.parametrize("provenance", ["human-written", "'human-written'", '"human-written"'])
@pytest.mark.parametrize("eol", ["\n", "\r\n"])
@pytest.mark.parametrize("published", [None, "single", "swarm"])
def test_census_requires_publication_and_reads_scalar_spellings(tmp_path, monkeypatch, provenance, eol, published):
    # L1-1/L1-2: failed-call audits and quoted marker mentions cannot establish publication;
    # YAML quotes and CRLF cannot hide the same false declaration once an answer is published.
    import sys

    folder = tmp_path / "demo"
    folder.mkdir()
    body = "Stage-2 call, 2026-11-04: explore · rejected\nA mention of research-swarm/v2.\n"
    body += "> ## Runner exploration — 2026-11-04\n> quoted answer\n"
    body += "```text\n## Runner exploration — 2026-11-04\nexample answer\n```\n"
    if published == "single":
        body += "## Runner exploration — 2026-11-04\n\nAccepted answer naming scripts/stage2.py.\n"
    elif published == "swarm":
        body += "<!-- research-swarm/v2 run abc123 -->\n## Research swarm\n"
        body += '```research-swarm/v2 manifest\n{"status": "incomplete"}\n```\n'
        body += "<!-- /research-swarm/v2 -->\n"
    (folder / "research.md").write_bytes((f"---\nprovenance: {provenance}\n---\n" + body).replace("\n", eol).encode())
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    if published:
        with pytest.raises(AssertionError, match="demo/research.md"):
            assert_active_model_research_has_no_false_human_provenance()
    else:
        assert_active_model_research_has_no_false_human_provenance()


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        ("# Research\nNo header.\n", "no frontmatter"),
        ("---\nprovenance: [\n---\n# Research\n", "malformed YAML"),
        ("---\n- provenance\n---\n# Research\n", "not a mapping"),
        ("---\nnull\n---\n# Research\n", "not a mapping"),
    ],
)
def test_census_names_unreadable_headers(tmp_path, monkeypatch, text, reason):
    import sys

    folder = tmp_path / "demo"
    folder.mkdir()
    (folder / "research.md").write_text(text, encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    with pytest.raises(AssertionError, match=rf"demo/research.md: unreadable header \({reason}\)"):
        assert_active_model_research_has_no_false_human_provenance()


def test_active_model_research_has_no_false_human_provenance():
    # Every research file outside the recorded uncorrected stock must meet the contract: a new
    # explore publication cannot add to the stock.
    assert_active_model_research_has_no_false_human_provenance(exempt=UNCORRECTED)


def test_uncorrected_stock_only_shrinks():
    # A listed file that now passes the census, or no longer is active research, leaves the list.
    failing = {finding.split(": ", 1)[0] for finding in census_findings()}
    stale = sorted(UNCORRECTED - failing)
    assert stale == [], f"remove corrected or archived research from UNCORRECTED: {stale}"


def test_census_exemption_is_limited_to_the_listed_files(tmp_path, monkeypatch):
    # The exemption names files; a new model-written file with a false header is still reported.
    for name in ("listed", "new"):
        folder = tmp_path / name
        folder.mkdir()
        (folder / "research.md").write_text(
            "---\nprovenance: human-written\n---\n# Research\n"
            "Stage-2 call, 2026-11-09: explore · endpoint glm-coding-plan\n"
            "## Runner exploration — 2026-11-09\n\nAccepted research.\n"
        )
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    with pytest.raises(AssertionError, match="new/research.md") as raised:
        assert_active_model_research_has_no_false_human_provenance(exempt=frozenset({"listed/research.md"}))
    assert "listed/research.md" not in str(raised.value)


@pytest.mark.parametrize("notice", stage2.skeleton_notices())
@pytest.mark.parametrize("published", [False, True])
def test_census_reports_opening_skeleton_notices(tmp_path, monkeypatch, notice, published):
    import sys

    folder = tmp_path / "demo"
    folder.mkdir()
    body = "# Research\n\n" + notice + "\n\n"
    if published:
        body += "Stage-2 call, 2026-11-05: explore · endpoint glm-coding-plan\n"
        body += "## Runner exploration — 2026-11-05\n\nAccepted research.\n"
    header = valid_research_header() if published else "---\nprovenance: human-written\n---\n"
    (folder / "research.md").write_text(header + body)
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    if published:
        with pytest.raises(AssertionError, match="demo/research.md: opening skeleton notice"):
            assert_active_model_research_has_no_false_human_provenance()
    else:
        assert_active_model_research_has_no_false_human_provenance()


def test_census_reports_undecodable_research(tmp_path, monkeypatch):
    import sys

    folder = tmp_path / "demo"
    folder.mkdir()
    (folder / "research.md").write_bytes(b"---\nprovenance: human-written\n---\n\xff")
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    try:
        with pytest.raises(AssertionError, match=r"demo/research.md: unreadable file \(not UTF-8\)"):
            assert_active_model_research_has_no_false_human_provenance()
    except UnicodeDecodeError as error:
        pytest.fail(f"The census must report the unreadable file instead of aborting: {error}")


def test_active_census_is_enabled():
    # L5-1: the repository guard must execute, rather than remain a bootstrap skip.
    marks = getattr(test_active_model_research_has_no_false_human_provenance, "pytestmark", [])
    assert not any(mark.name in {"skip", "skipif"} for mark in marks), "enable the active-research census"
    test_active_model_research_has_no_false_human_provenance()


@pytest.mark.parametrize("error_type", [PermissionError, FileNotFoundError, OSError])
def test_census_reports_read_errors(tmp_path, monkeypatch, error_type):
    paths = []
    for name in ("a-unreadable", "z-later"):
        folder = tmp_path / name
        folder.mkdir()
        path = folder / "research.md"
        path.write_text("# Missing frontmatter\n")
        paths.append(path)
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    original_read = Path.read_bytes

    def read_bytes(path):
        if path == paths[0]:
            raise error_type("planted read failure")
        return original_read(path)

    monkeypatch.setattr(Path, "read_bytes", read_bytes)
    try:
        findings = census_findings()
    except OSError as error:
        pytest.fail(f"The census must report the unreadable path and continue: {error}")
    assert any(line.startswith("a-unreadable/research.md: unreadable file") for line in findings)
    assert "z-later/research.md: unreadable header (no frontmatter)" in findings
    with pytest.raises(AssertionError, match="z-later/research.md") as raised:
        assert_active_model_research_has_no_false_human_provenance(exempt=frozenset({"a-unreadable/research.md"}))
    assert "a-unreadable/research.md" not in str(raised.value)


def test_census_is_read_only_without_history(tmp_path, monkeypatch):
    import builtins
    import io
    import os
    import subprocess

    import research_census as census

    paths = []
    for name, header in (("valid", valid_research_header()), ("fault", "---\nprovenance: human-written\n---\n")):
        folder = tmp_path / name
        folder.mkdir()
        path = folder / "research.md"
        path.write_text(
            header + "# Research\nStage-2 call, 2026-11-05: explore · endpoint glm-coding-plan\n"
            "## Runner exploration — 2026-11-05\n\nAccepted research.\n"
        )
        paths.append(path)
    before = {path: path.read_bytes() for path in paths}
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)

    def forbidden(*_args, **_kwargs):
        pytest.fail("The census must only read current files, without writes or history commands")

    def read_only_open(original):
        def checked(file, mode="r", *args, **kwargs):
            if any(flag in mode for flag in "wax+"):
                forbidden()
            return original(file, mode, *args, **kwargs)

        return checked

    # Import dependencies before denying process creation; the fixture deliberately has no Git history.
    assert census.stage2 is stage2
    with monkeypatch.context() as guard:
        guard.setattr(builtins, "open", read_only_open(builtins.open))
        guard.setattr(io, "open", read_only_open(io.open))
        guard.setattr(subprocess, "Popen", forbidden)
        guard.setattr(os, "system", forbidden)
        for name in ("write_bytes", "write_text", "unlink", "rename", "replace", "touch"):
            guard.setattr(Path, name, forbidden)
        findings = census_findings()
    assert findings and all(line.startswith("fault/research.md: ") for line in findings)
    assert any("provenance: expected" in line for line in findings)
    assert {path: path.read_bytes() for path in paths} == before


@pytest.mark.parametrize("endpoint", ["opencode-go", "newly-admitted-endpoint", "future_pi_2"])
def test_census_accepts_unnamed_endpoint_producers(tmp_path, monkeypatch, endpoint):
    folder = tmp_path / "demo"
    folder.mkdir()
    path = folder / "research.md"
    header = valid_research_header().replace("name: claude-code", "name: pi")
    body = (
        f"# Research\nStage-2 call, 2026-11-05: explore · endpoint {endpoint}\n"
        "## Runner exploration — 2026-11-05\n\nAccepted research.\n"
    )
    path.write_text(header + body)
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    assert_active_model_research_has_no_false_human_provenance()
    path.write_text(header.replace("name: pi", "name: codex") + body)
    with pytest.raises(AssertionError, match="missing publication program/date"):
        assert_active_model_research_has_no_false_human_provenance()


def valid_research_header():
    return (
        "---\nprovenance: ai-drafted-reviewed\n"
        'produced_by: {kind: llm-session, name: claude-code, version: "2026-11-05"}\n'
        "review: {status: pending, approved_by: null, approved_at: null}\n"
        "date: 2026-11-04\nlast_reviewed: 2026-11-04\nupdated: 2026-11-05\n---\n"
    )


@pytest.mark.parametrize("eol", ["\n", "\r\n"])
@pytest.mark.parametrize("route", ["single", "swarm"])
def test_census_reads_real_line_endings(tmp_path, monkeypatch, eol, route):
    folder = tmp_path / "demo"
    folder.mkdir()
    body = "# Research\n"
    if route == "single":
        body += "Stage-2 call, 2026-11-05: explore · endpoint glm-coding-plan\n"
        body += "## Runner exploration — 2026-11-05\n\nAccepted answer.\n"
    else:
        body += "<!-- research-swarm/v2 run abc123 -->\n## Research swarm\n"
        body += "<!-- /research-swarm/v2 -->\n"
    text = valid_research_header() + body
    if route == "swarm":
        text = text.replace("name: claude-code", "name: stage2-research-swarm")
    path = folder / "research.md"
    path.write_bytes(text.replace("\n", eol).encode())
    # Do not let universal-newline translation hide a broken CRLF regex in the census.
    original_read = Path.read_text
    monkeypatch.setattr(
        Path,
        "read_text",
        lambda self, *a, **kw: self.read_bytes().decode() if self == path else original_read(self, *a, **kw),
    )
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    assert_active_model_research_has_no_false_human_provenance()
    path.write_bytes(text.replace("ai-drafted-reviewed", "human-written").replace("\n", eol).encode())
    with pytest.raises(AssertionError, match="provenance: expected"):
        assert_active_model_research_has_no_false_human_provenance()


@pytest.mark.parametrize(
    "fault",
    [
        "missing-producer",
        "model-name",
        "wrong-program",
        "compound-version",
        "stale-version",
        "producer-kind",
        "missing-review",
        "approved-review",
        "missing-provenance",
        "duplicate-producer",
        "duplicate-nested-producer",
        "duplicate-nested-review",
        "invalid-date",
        "stale-updated",
        "missing-updated",
        "missing-reviewed",
    ],
)
def test_census_rejects_incomplete_publication_metadata(tmp_path, monkeypatch, fault):
    text = valid_research_header()
    if fault == "missing-producer":
        text = re.sub(r"(?m)^produced_by:.*\n", "", text)
    elif fault == "model-name":
        text = text.replace("name: claude-code", "name: glm-5.3-flash")
    elif fault == "wrong-program":
        text = text.replace("name: claude-code", "name: codex")
    elif fault == "compound-version":
        text = text.replace('version: "2026-11-05"', 'version: "GLM 5.3 Flash, 2026-11-05"')
    elif fault == "stale-version":
        text = text.replace('version: "2026-11-05"', 'version: "2026-11-04"')
    elif fault == "producer-kind":
        text = text.replace("kind: llm-session", "kind: human")
    elif fault == "missing-review":
        text = re.sub(r"(?m)^review:.*\n", "", text)
    elif fault == "approved-review":
        text = text.replace(
            "status: pending, approved_by: null, approved_at: null",
            "status: approved, approved_by: maintainer, approved_at: 2026-11-05",
        )
    elif fault == "missing-provenance":
        text = text.replace("provenance: ai-drafted-reviewed\n", "")
    elif fault == "duplicate-producer":
        text = text.replace(
            "review:", 'produced_by: {kind: llm-session, name: claude-code, version: "2026-11-05"}\nreview:'
        )
    elif fault == "duplicate-nested-producer":
        text = text.replace("name: claude-code", "name: codex, name: claude-code")
    elif fault == "duplicate-nested-review":
        text = text.replace("status: pending", "status: approved, status: pending")
    elif fault == "invalid-date":
        text = text.replace("date: 2026-11-04", "date: 2026-02-30")
    elif fault == "stale-updated":
        text = text.replace("updated: 2026-11-05", "updated: 2026-11-03")
    elif fault == "missing-updated":
        text = text.replace("updated: 2026-11-05\n", "")
    elif fault == "missing-reviewed":
        text = text.replace("last_reviewed: 2026-11-04\n", "")
    text += "# Research\nStage-2 call, 2026-11-05: explore · endpoint glm-coding-plan\n"
    text += "## Runner exploration — 2026-11-05\n\nAccepted research.\n"
    folder = tmp_path / "demo"
    folder.mkdir()
    (folder / "research.md").write_text(text)
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    with pytest.raises(AssertionError, match="demo/research.md"):
        assert_active_model_research_has_no_false_human_provenance()


def test_census_accepts_and_checks_every_producer(tmp_path, monkeypatch):
    import research_census as census

    producers = [
        {"kind": "llm-session", "name": "codex", "version": "2026-11-04", "model": "gpt-6.1-sol"},
        {"kind": "llm-session", "name": "pi", "version": "2026-11-05", "model": "GLM 5.3 Flash"},
    ]
    folder = tmp_path / "demo"
    folder.mkdir()
    text = re.sub(
        r"produced_by:.*",
        "produced_by: " + yaml.safe_dump(producers, default_flow_style=True).strip(),
        valid_research_header(),
    )
    path = folder / "research.md"
    path.write_text(text + "# Research\n")
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    assert_active_model_research_has_no_false_human_provenance()
    for fault in (
        text.replace("name: pi", "name: unknown"),
        text.replace("name: pi", "name: [pi]"),
        text.replace("2026-11-05", "2026-11-99", 1),
        text.replace("name: pi", "name: codex, name: pi"),
        text.replace("kind: llm-session", "kind: human", 1),
        text.replace("version: '2026-11-04'", "version: '2026-10-01'"),
    ):
        assert fault != text, "each fixture must plant its intended metadata fault"
        path.write_text(fault + "# Research\n")
        with pytest.raises(AssertionError, match="demo/research.md"):
            assert_active_model_research_has_no_false_human_provenance()
    assert census.metadata_problems({"produced_by": []}, "produced_by: []")


@pytest.mark.parametrize(
    "opener,closer", [("```markdown", "````"), ("   ```text", "   ```"), ("~~~text", "~~~~"), ("```", "")]
)
@pytest.mark.parametrize("eol", ["\n", "\r\n"])
@pytest.mark.parametrize("kind", ["single", "swarm"])
def test_census_ignores_commonmark_fenced_publication_examples(tmp_path, opener, closer, eol, kind):
    import research_census as census

    example = (
        "Stage-2 call, 2026-11-05: explore · endpoint glm-coding-plan\n\n"
        "## Runner exploration — 2026-11-05\n\nExample answer.\n"
    )
    if kind == "swarm":
        example = "<!-- research-swarm/v2 run abc123 -->\n## Research swarm\nExample.\n<!-- /research-swarm/v2 -->\n"
    body = "# Human research\n\n" + opener + "\n" + example + closer + "\n"
    assert census.publication_evidence(body.replace("\n", eol)) == (None, None), (
        "a fenced example cannot establish runner publication"
    )
    path = tmp_path / "research.md"
    path.write_bytes(("---\nprovenance: human-written\n---\n" + body).replace("\n", eol).encode())
    assert census.census_findings([path], tmp_path) == [], "unpublished human research must pass the census"
