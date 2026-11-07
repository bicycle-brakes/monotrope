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
        except (OSError, UnicodeDecodeError):
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
        try:
            historical = normalise.historical_research(REPO_ROOT, relative) if (REPO_ROOT / ".git").exists() else None
            required = normalise.known_producers(text.encode("utf-8"), historical=historical)
        except (ValueError, OSError, yaml.YAMLError) as error:
            affected.append(f"{relative}: producer history unreadable: {error}")
            required = []
        if program or model_written or required or header.get("provenance") == "ai-drafted-reviewed":
            affected.extend(
                f"{relative}: {problem}"
                for problem in normalise.metadata_problems(
                    header, frontmatter.group(1), program, publication_day, required_producers=required
                )
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
        # Independently compare the backfill with pre-correction attribution and
        # accepted audited models, so a complete-looking collapsed header fails.
        from normalise_active_research import historical_research, known_producers, metadata_problems

        path = PLANS / name / "research.md"
        raw_header = path.read_text().split("---", 2)[1]
        history = historical_research(REPO_ROOT, path.relative_to(REPO_ROOT).as_posix())
        required = known_producers(path.read_bytes(), historical=history)
        assert metadata_problems(header, raw_header, required_producers=required) == [], name


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


def test_normaliser_checks_authorised_scope(tmp_path, monkeypatch):
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
    monkeypatch.setattr(normalise, "base_research_paths", lambda _: {"plans/changes/demo/research.md"})
    assert check(tmp_path) == [demo / "research.md"]
    foreign = folder.parent / "new-lane"
    foreign.mkdir()
    (foreign / "research.md").write_text("not approved")
    assert check(tmp_path) == [demo / "research.md"], "post-base research is outside the one-time batch"
    (folder / "plan.md").write_text("")
    with pytest.raises(ValueError, match="demo/research.md: outside authorised"):
        check(tmp_path)


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
    monkeypatch.setattr(normalise, "base_research_paths", lambda _: {p.relative_to(tmp_path).as_posix() for p in paths})
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


@pytest.mark.parametrize("name", ["go-access-point", "interview-context"])
def test_normaliser_restores_merge_base_contributors(name):
    import normalise_active_research as normalise

    relative = f"plans/changes/{name}/research.md"
    historical = normalise.historical_research(REPO_ROOT, relative)
    assert historical is not None, "the regression needs the original merge-base attribution"
    original = (REPO_ROOT / relative).read_bytes()
    corrected = normalise.normalised_research(original, correction_day="2026-11-07", historical=historical)
    records = yaml.safe_load(corrected.decode().split("---", 2)[1])["produced_by"]
    assert isinstance(records, list), "retain the original contributors alongside the accepted runner model"
    assert {
        "kind": "llm-session",
        "name": "claude-code",
        "version": "2026-10-31" if name == "go-access-point" else "2026-10-14",
        "model": "glm-5.3-flash",
    } in records, "retain the model from the accepted runner call"
    if name == "go-access-point":
        for model in ("GLM 5.3 Flash", "Claude Haiku 5.5"):
            assert {"kind": "llm-session", "name": "pi", "version": "2026-10-31", "model": model} in records
    else:
        assert {"kind": "llm-session", "name": "codex", "version": "2026-10-14"} in records
    assert corrected.split(b"---", 2)[2] == original.split(b"---", 2)[2]
    assert normalise.normalised_research(corrected, correction_day="2026-11-08", historical=historical) == corrected


def test_batch_restores_models_before_reaching_fixed_point(tmp_path, monkeypatch):
    import normalise_active_research as normalise

    folder = tmp_path / "plans/changes/demo"
    folder.mkdir(parents=True)
    path = folder / "research.md"
    historical = valid_research_header().replace('version: "2026-11-05"', 'version: "Opus 5.5, 2026-11-05"').encode()
    body = (
        "# Research\nStage-2 call, 2026-11-05: explore · endpoint glm-coding-plan · model glm-5.3-flash\n"
        "## Runner exploration — 2026-11-05\n\nAccepted research.\n"
    ).encode()
    path.write_bytes(valid_research_header().encode() + body)
    monkeypatch.setattr(normalise, "authorised_research", lambda _: [path])
    monkeypatch.setattr(normalise, "historical_research", lambda *_: historical + b"# Research\n")
    changes = normalise.prepare_batch(tmp_path, correction_day="2026-11-07")
    assert len(changes) == 1, "collapsed attribution must still need a correction"
    records = yaml.safe_load(changes[0][1].decode().split("---", 2)[1])["produced_by"]
    assert isinstance(records, list), "the batch must preserve historical and audited contributions as a list"
    assert {record.get("model") for record in records} == {"Opus 5.5", "glm-5.3-flash"}, (
        "restore historical and published models"
    )
    path.write_bytes(changes[0][1])
    assert normalise.prepare_batch(tmp_path, correction_day="2026-11-08") == [], (
        "the applied batch must reach a fixed point"
    )


@pytest.mark.parametrize("lost", ["model", "program"])
def test_census_rejects_lost_historical_contributors(tmp_path, monkeypatch, lost):
    import normalise_active_research as normalise

    folder = tmp_path / "demo"
    folder.mkdir()
    path = folder / "research.md"
    text = valid_research_header()
    history = text.replace("name: claude-code", "name: codex") if lost == "program" else text
    history = history.replace('version: "2026-11-05"', 'version: "Opus 5.5, 2026-11-05"')
    path.write_text(text + "# Research\n")
    (tmp_path / ".git").write_text("fixture: history supplied below")
    monkeypatch.setattr(normalise, "historical_research", lambda *_: (history + "# Research\n").encode())
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    try:
        with pytest.raises(AssertionError, match="demo/research.md: produced_by: missing known contribution"):
            assert_active_model_research_has_no_false_human_provenance()
    except AttributeError as error:
        pytest.fail(f"the census must compare each header with known historical producers: {error}")
    corrected = normalise.normalised_research(
        path.read_bytes(), correction_day="2026-11-07", historical=(history + "# Research\n").encode()
    )
    path.write_bytes(corrected)
    assert_active_model_research_has_no_false_human_provenance()


def test_new_change_folder_keeps_census_green(tmp_path, monkeypatch):
    from types import SimpleNamespace

    import normalise_active_research as normalise

    folder = tmp_path / "plans/changes/explore-provenance"
    folder.mkdir(parents=True)
    (folder / "plan.md").write_text("- `plans/changes/demo/research.md` — approved\n")
    demo = folder.parent / "demo"
    demo.mkdir()
    (demo / "research.md").write_text(valid_research_header() + "# Research\n")
    # Git's frozen inventory is unchanged when the new-change command adds a skeleton.
    monkeypatch.setattr(
        normalise.subprocess,
        "run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stdout=b"plans/changes/demo/research.md\n"),
    )
    before = normalise.authorised_research(tmp_path)
    fresh = folder.parent / "future-lane"
    fresh.mkdir()
    (fresh / "research.md").write_text("---\nprovenance: human-written\n---\n# Research\n")
    try:
        after = normalise.authorised_research(tmp_path)
    except ValueError as error:
        pytest.fail(f"a post-base change folder must keep verification green: {error}")
    assert after == before == [demo / "research.md"]
    monkeypatch.setattr(sys.modules[__name__], "PLANS", folder.parent)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    assert_active_model_research_has_no_false_human_provenance()
