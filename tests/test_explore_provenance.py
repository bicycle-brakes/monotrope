"""Active model-written research has truthful, complete publication metadata."""

from __future__ import annotations

import re
import sys
from collections.abc import Mapping
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PLANS = REPO_ROOT / "plans" / "changes"
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import stage2  # noqa: E402


def active_research_files() -> list[Path]:
    archive = PLANS / "archive"
    return sorted(path for path in PLANS.glob("*/research.md") if archive not in path.parents)


def assert_active_model_research_has_no_false_human_provenance() -> None:
    try:
        import normalise_active_research as normalise
    except ModuleNotFoundError as error:
        pytest.fail(f"Active research needs the complete metadata census and normaliser: {error}")
    affected = []
    for path in active_research_files():
        relative = path.relative_to(REPO_ROOT).as_posix()
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            affected.append(f"{relative}: unreadable file (not UTF-8)")
            continue
        frontmatter = normalise.FRONTMATTER.match(text)
        if frontmatter is None:
            affected.append(f"{relative}: unreadable header (no frontmatter)")
            continue
        try:
            header = yaml.safe_load(frontmatter.group(1))
        except (yaml.YAMLError, ValueError):
            affected.append(f"{relative}: unreadable header (malformed YAML)")
            continue
        if not isinstance(header, Mapping):
            affected.append(f"{relative}: unreadable header (not a mapping)")
            continue
        body = text[frontmatter.end() :]
        try:
            program, publication_day = normalise.publication_evidence(body)
        except ValueError as error:
            affected.append(f"{relative}: {error}")
            program, publication_day = None, None
        producer = header.get("produced_by")
        model_written = normalise.model_attribution(producer)
        if program or model_written or header.get("provenance") == "ai-drafted-reviewed":
            affected.extend(
                f"{relative}: {problem}"
                for problem in normalise.metadata_problems(header, frontmatter.group(1), program, publication_day)
            )
            try:
                notices = stage2.research_opening_notices(text, frontmatter.end())
            except AttributeError as error:
                pytest.fail(f"The census requires the publisher's opening-notice detector: {error}")
            if notices:
                affected.append(f"{relative}: opening skeleton notice over published research")
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
    assert_active_model_research_has_no_false_human_provenance()


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


def test_named_backfills_have_no_opening_notices(monkeypatch):
    # L5-2: check the real four additional active backfills, including already-corrected headers.
    paths = [
        PLANS / name / "research.md"
        for name in ("run-report", "interview-context", "fail-fast-attempts", "go-access-point")
    ]
    monkeypatch.setattr(sys.modules[__name__], "active_research_files", lambda: paths)
    assert_active_model_research_has_no_false_human_provenance()


def test_loop_backfill_stamp_reaches_its_correction_day():
    # L5-6: use the existing gate's real reference date, so this check does not age with the calendar.
    from datetime import date

    import check_frontmatter_current as current

    relative = "plans/changes/loop-until-clean/research.md"
    reference, source = current.reference_dates(REPO_ROOT, [relative], date.today())[relative]
    reference = max(reference, date(2026, 11, 5))  # the recorded repair day, not the decision day
    updated = current.read_updated((REPO_ROOT / relative).read_text())
    assert isinstance(updated, date) and updated >= reference, f"backfill stamp must reach {reference} ({source})"


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


def test_additional_backfills_identify_the_program_and_publication_day():
    expected = {
        "run-report": "2026-10-28",
        "fail-fast-attempts": "2026-10-28",
        "interview-context": "2026-10-14",
        "go-access-point": "2026-10-31",
    }
    for name, day in expected.items():
        header = yaml.safe_load((PLANS / name / "research.md").read_text().split("---", 2)[1])
        records = header["produced_by"]
        records = records if isinstance(records, list) else [records]
        expected = {"kind": "llm-session", "name": "claude-code", "version": day}
        assert any(all(record.get(key) == value for key, value in expected.items()) for record in records), name
        # Prior contributions may accompany this publication, and every entry must
        # remain a complete program/date record rather than a collapsed model label.
        from normalise_active_research import metadata_problems

        raw_header = (PLANS / name / "research.md").read_text().split("---", 2)[1]
        assert metadata_problems(header, raw_header) == [], name


def test_normaliser_preserves_research_and_is_idempotent():
    try:
        from normalise_active_research import normalised_research
    except ModuleNotFoundError as error:
        pytest.fail(f"An evidence-based active research normaliser is required: {error}")
    original = (
        (
            valid_research_header()
            .replace("name: claude-code", "name: codex")
            .replace('version: "2026-11-05"', 'version: "gpt-6.1-sol, 2026-11-05"')
            + "# Research\n\nAuthored prose.\n"
            + "Stage-2 call, 2026-11-05: explore · endpoint glm-coding-plan\n"
            + "## Runner exploration — 2026-11-05\n\nAccepted research.\n"
        )
        .replace("\n", "\r\n")
        .encode()
    )
    corrected = normalised_research(original, correction_day="2026-11-06")
    assert b'name: claude-code, version: "2026-11-05"' in corrected
    assert b"updated: 2026-11-06" in corrected
    assert corrected.split(b"---", 2)[2] == original.split(b"---", 2)[2]
    assert normalised_research(corrected, correction_day="2026-11-06") == corrected


def test_normaliser_checks_authorised_scope(tmp_path):
    import normalise_active_research as normalise

    check = getattr(normalise, "authorised_research", None)
    assert callable(check), "normalisation must check the maintainer-approved active research inventory"
    folder = tmp_path / "plans/changes/explore-provenance"
    folder.mkdir(parents=True)
    (folder / "plan.md").write_text("- `plans/changes/demo/research.md` — approved\n")
    demo = folder.parent / "demo"
    demo.mkdir()
    (demo / "research.md").write_text("approved")
    archive = folder.parent / "archive"
    archive.mkdir()
    (archive / "research.md").write_text("historical")
    assert check(tmp_path) == [demo / "research.md"]
    foreign = folder.parent / "new-lane"
    foreign.mkdir()
    (foreign / "research.md").write_text("not approved")
    with pytest.raises(ValueError, match="new-lane/research.md: outside authorised"):
        check(tmp_path)
    # The real active inventory must also match the newly approved scope.
    assert set(check(REPO_ROOT)) == set(active_research_files())


def test_normaliser_keeps_all_known_producers():
    import normalise_active_research as normalise

    original = (
        valid_research_header()
        .replace(
            'name: claude-code, version: "2026-11-05"',
            'name: pi, version: "GLM 5.3 Flash and Claude Haiku 5.5, 2026-11-05"',
        )
        .encode()
        + b"# Research\n\nAuthored research.\n"
    )
    corrected = normalise.normalised_research(original, correction_day="2026-11-06")
    header = yaml.safe_load(corrected.decode().split("---", 2)[1])
    assert header["produced_by"] == [
        {"kind": "llm-session", "name": "pi", "version": "2026-11-05", "model": "GLM 5.3 Flash"},
        {"kind": "llm-session", "name": "pi", "version": "2026-11-05", "model": "Claude Haiku 5.5"},
    ], "normalisation must retain both known models and their actual program/date"
    assert normalise.normalised_research(corrected, correction_day="2026-11-07") == corrected
    # Already-collapsed branch metadata cannot serve as its own historical evidence.
    collapsed = original.replace(b'pi, version: "GLM 5.3 Flash and Claude Haiku 5.5,', b'claude-code, version: "')
    recovered = normalise.normalised_research(collapsed, correction_day="2026-11-06", historical=original)
    assert yaml.safe_load(recovered.decode().split("---", 2)[1])["produced_by"] == header["produced_by"]


def test_census_accepts_and_checks_every_producer(tmp_path, monkeypatch):
    import normalise_active_research as normalise

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
    assert normalise.metadata_problems({"produced_by": []}, "produced_by: []")


def test_normaliser_preserves_unrelated_metadata_bytes():
    import normalise_active_research as normalise

    original = (
        valid_research_header()
        .replace('name: claude-code, version: "2026-11-05"', 'name: pi, version: "GLM 5.3 Flash, 2026-11-05"')
        .replace("---\nprovenance:", '---\nowner: "Owner" # keep\nclass: bounded\nstatus: draft\nprovenance:', 1)
    )
    original = (original + "# Research\n\nAuthored\rprose.\n").replace("\n", "\r\n").encode()
    corrected = normalise.normalised_research(original, correction_day="2026-11-06")
    for line in (b'owner: "Owner" # keep\r\n', b"class: bounded\r\n", b"status: draft\r\n"):
        assert line in corrected
    assert corrected.split(b"---", 2)[2] == original.split(b"---", 2)[2]


@pytest.mark.parametrize("field", ["name: unknown", 'version: "unknown"', 'version: "2026-99-05"'])
def test_normaliser_refuses_unknown_historical_metadata(field):
    import normalise_active_research as normalise

    original = valid_research_header()
    key = field.split(":")[0]
    original = re.sub(rf'{key}: (?:"[^"]*"|claude-code)', field, original)
    original += "# Research\n"
    with pytest.raises(ValueError, match="historical|evidence"):
        normalise.normalised_research(original.encode(), correction_day="2026-11-06")


def test_normaliser_dry_run_and_batch_preparation(tmp_path, monkeypatch, capsys):
    import normalise_active_research as normalise

    folder = tmp_path / "plans/changes/explore-provenance"
    folder.mkdir(parents=True)
    paths = []
    for name in ("a", "b"):
        directory = folder.parent / name
        directory.mkdir()
        path = directory / "research.md"
        path.write_text(
            valid_research_header().replace('version: "2026-11-05"', 'version: "Opus 5.5, 2026-11-05"') + "# Research\n"
        )
        paths.append(path)
    (folder / "plan.md").write_text("\n".join(f"- `{p.relative_to(tmp_path)}` — approved" for p in paths))
    history = getattr(normalise, "historical_research", None)
    assert callable(history), "batch preparation must recover pre-correction attribution from Git"
    monkeypatch.setattr(normalise, "historical_research", lambda *_: None)
    before = [p.read_bytes() for p in paths]
    normalise.main(tmp_path, [])
    assert [p.read_bytes() for p in paths] == before, "default invocation must only report corrections"
    assert "plans/changes/a/research.md" in capsys.readouterr().out
    paths[1].write_text("invalid header")
    with pytest.raises(ValueError, match="b/research.md: no research frontmatter"):
        normalise.main(tmp_path, ["--write"])
    assert paths[0].read_bytes() == before[0], "prepare the entire batch before the first write"
    paths[1].write_bytes(before[1])
    normalise.main(tmp_path, ["--write"])
    after = [p.read_bytes() for p in paths]
    assert after != before
    normalise.main(tmp_path, ["--write"])
    assert [p.read_bytes() for p in paths] == after
