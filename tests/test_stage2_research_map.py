"""Finder union and neighbour membership counterexamples, without model calls."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
OWN = "plans/changes/own/spec.md"
ACTIVE = "plans/changes/adjacent/spec.md"
ARCHIVE = "plans/changes/archive/2026-10-01-old/spec.md"
LIVING = "plans/specs/capability/spec.md"


def module():
    import stage2_research_map

    return stage2_research_map


def empty(merged=False, reports=None):
    categories = ("code", "rules", "tests", "neighbours")
    if not merged:
        return {category: [{"not_read": "no locator found"}] for category in categories}
    reports = reports if reports is not None else trio()
    result = {}
    for category in categories:
        origins = [
            {"finder": seat, "reason": entry["not_read"]}
            for seat, report in reports.items()
            for entry in report[category]
            if "not_read" in entry
        ]
        result[category] = [{"not_read": origins}] if origins else []
    return result


def finder(path, reference="Scope", reason="locate"):
    return {"path": path, "reference": reference, "reason": reason}


def merged(path, origins, reference="Scope"):
    return {
        "path": path,
        "reference": reference,
        "origins": [{"finder": seat, "reason": reason} for seat, reason in origins],
    }


def sources():
    return {
        path: b"# Scope\nbody\n"
        for path in (
            OWN,
            ACTIVE,
            ARCHIVE,
            LIVING,
            "plans/changes/adjacent/design.md",
            "plans/changes/own/design.md",
            "docs/elsewhere.md",
        )
    }


def trio():
    return {seat: empty() for seat in ("deepseek-finder", "mimo-finder", "haiku-finder")}


@pytest.mark.parametrize(
    "header", [{}, {"neighbours": None}, {"neighbours": "x"}, {"neighbours": [1]}, {"neighbours": [ACTIVE, ACTIVE]}]
)
def test_map_given_neighbour_header_missing_and_empty_are_distinct(header):
    with pytest.raises(module().ResearchMapError) as failure:
        module().validate_given_neighbours(header, sources(), OWN)
    assert failure.value.exit_code == 2
    assert "neighbours: []" in str(failure.value)
    assert module().validate_given_neighbours({"neighbours": []}, sources(), OWN) == []


@pytest.mark.parametrize("path", [ACTIVE, ARCHIVE, LIVING])
def test_map_given_neighbours_accept_exact_existing_frozen_spec_forms(path):
    assert module().validate_given_neighbours({"neighbours": [path]}, sources(), OWN) == [path]


@pytest.mark.parametrize(
    "path",
    [
        OWN,
        "templates/spec.md",
        "plans/changes/adjacent/design.md",
        "plans/changes/absent/spec.md",
        "../plans/changes/adjacent/spec.md",
        "/plans/changes/adjacent/spec.md",
        "plans/changes/archive/spec.md",
        "plans/changes/archive/2026-02-30-old/spec.md",
        "plans/specs/capability/nested/spec.md",
    ],
)
def test_map_given_neighbours_refuse_own_missing_escape_and_non_spec_forms(path):
    frozen = sources() | {path: b"# Scope\n"}
    if path == "plans/changes/absent/spec.md":
        del frozen[path]
    with pytest.raises(module().ResearchMapError) as failure:
        module().validate_given_neighbours({"neighbours": [path]}, frozen, OWN)
    assert failure.value.exit_code == 2


def overlapping():
    reports = trio()
    for seat, reason in (("deepseek-finder", "calls"), ("mimo-finder", "boundary"), ("haiku-finder", "rule")):
        reports[seat]["code"] = [finder("src/app.py", "run", reason)]
    result = empty(merged=True, reports=reports)
    result["code"] = [
        merged(
            "src/app.py", [("haiku-finder", "rule"), ("deepseek-finder", "calls"), ("mimo-finder", "boundary")], "run"
        )
    ]
    return reports, result, sources() | {"src/app.py": b"def run():\n    return 1\n"}


def test_map_exact_union_retains_all_origins_without_persisting_frozen_snapshots():
    reports, merge, frozen = overlapping()
    result = module().merge_research_map(reports, merge, frozen, [], OWN)
    assert result["scope"] == [["code", "src/app.py", "run"]]
    entry = result["entries"][0]
    assert entry["status"] == "resolved"
    assert len(entry["origins"]) == 3
    assert {item["reason"] for item in entry["origins"]} == {"calls", "boundary", "rule"}
    assert entry["extent"] == {"start_line": 1, "end_line": 2}
    assert "excerpt" not in entry and len(entry["excerpt_sha256"]) == 64


@pytest.mark.parametrize(
    "fault", ["drop", "add", "duplicate", "drop-origin", "change-reason", "invent-origin", "duplicate-origin"]
)
def test_map_merge_cannot_change_keys_or_finder_evidence(fault):
    reports, merge, frozen = overlapping()
    if fault == "drop":
        merge["code"] = []
    elif fault == "add":
        merge["rules"] = [merged("new.py", [("haiku-finder", "new")])]
    elif fault == "duplicate":
        merge["code"].append(copy.deepcopy(merge["code"][0]))
    elif fault == "drop-origin":
        merge["code"][0]["origins"].pop()
    elif fault == "change-reason":
        merge["code"][0]["origins"][0]["reason"] = "changed"
    elif fault == "invent-origin":
        merge["code"][0]["origins"][0]["finder"] = "invented"
    else:
        merge["code"][0]["origins"].append(copy.deepcopy(merge["code"][0]["origins"][0]))
    with pytest.raises(module().ResearchMapError) as failure:
        module().merge_research_map(reports, merge, frozen, [], OWN)
    assert failure.value.exit_code == 1


def test_map_unresolved_locator_stays_visible_but_grants_no_scope_or_neighbour():
    reports = trio()
    reports["mimo-finder"]["neighbours"] = [finder(ACTIVE, "Absent")]
    merge = empty(merged=True, reports=reports)
    merge["neighbours"] += [merged(ACTIVE, [("mimo-finder", "locate")], "Absent")]
    result = module().merge_research_map(reports, merge, sources(), [], OWN)
    assert result["entries"][0]["status"] == "unresolved"
    assert result["scope"] == result["neighbours"] == result["gaps"] == []


def test_map_given_neighbour_is_inserted_even_when_all_finders_omit_it():
    result = module().merge_research_map(trio(), empty(merged=True), sources(), [ACTIVE], OWN)
    assert result["entries"] == []
    assert result["neighbours"] == [{"path": ACTIVE, "status": "given", "map_keys": []}]


@pytest.mark.parametrize(
    "path,spec",
    [
        ("plans/changes/adjacent/design.md", ACTIVE),
        ("plans/changes/archive/2026-10-01-old/plan.md", ARCHIVE),
        ("plans/specs/capability/spec.md", LIVING),
    ],
)
def test_map_resolved_neighbour_artifact_maps_to_frozen_sibling_spec(path, spec):
    reports = trio()
    reports["deepseek-finder"]["neighbours"] = [finder(path)]
    merge = empty(merged=True, reports=reports)
    merge["neighbours"] += [merged(path, [("deepseek-finder", "locate")])]
    result = module().merge_research_map(reports, merge, sources() | {path: b"# Scope\nbody\n"}, [], OWN)
    assert result["neighbours"] == [{"path": spec, "status": "suggested", "map_keys": [["neighbours", path, "Scope"]]}]
    assert not result["gaps"]


@pytest.mark.parametrize(
    "path,status,gaps",
    [
        ("plans/changes/own/design.md", "self", 0),
        ("docs/elsewhere.md", "no-spec", 1),
        ("plans/changes/no-spec/design.md", "no-spec", 1),
    ],
)
def test_map_own_and_spec_less_artifacts_do_not_gain_neighbour_status(path, status, gaps):
    reports = trio()
    reports["haiku-finder"]["neighbours"] = [finder(path)]
    merge = empty(merged=True, reports=reports)
    merge["neighbours"] += [merged(path, [("haiku-finder", "locate")])]
    result = module().merge_research_map(reports, merge, sources() | {path: b"# Scope\n"}, [], OWN)
    assert not result["neighbours"]
    assert result["entries"][0]["neighbour_status"] == status
    assert len(result["gaps"]) == gaps


def test_map_given_status_overrides_suggestion_and_merges_artifact_keys():
    reports = trio()
    reports["haiku-finder"]["neighbours"] = [finder(ACTIVE), finder("plans/changes/adjacent/design.md")]
    merge = empty(merged=True, reports=reports)
    merge["neighbours"] += [
        merged(path, [("haiku-finder", "locate")]) for path in (ACTIVE, "plans/changes/adjacent/design.md")
    ]
    result = module().merge_research_map(reports, merge, sources(), [ACTIVE], OWN)
    assert len(result["neighbours"]) == 1
    assert result["neighbours"][0]["status"] == "given"
    assert len(result["neighbours"][0]["map_keys"]) == 2
    assert not result["gaps"]


def test_map_raw_json_reports_use_the_same_exact_union_validation():
    reports, merge, frozen = overlapping()
    result = module().merge_research_map(
        {seat: json.dumps(report) for seat, report in reports.items()}, json.dumps(merge), frozen, [], OWN
    )
    assert result["scope"] == [["code", "src/app.py", "run"]]
    assert len(result["entries"][0]["origins"]) == 3


@pytest.mark.parametrize("target", ["finder", "merge"])
def test_map_duplicate_raw_json_keys_fail_preparation(target):
    reports, merge, frozen = overlapping()
    if target == "finder":
        report = reports["haiku-finder"]
        reports["haiku-finder"] = json.dumps(report)[:-1] + ',"code":' + json.dumps(report["code"]) + "}"
    else:
        merge = json.dumps(merge)[:-1] + ',"code":' + json.dumps(merge["code"]) + "}"
    with pytest.raises(module().ResearchMapError) as failure:
        module().merge_research_map(reports, merge, frozen, [], OWN)
    assert failure.value.exit_code == 1


@pytest.mark.parametrize("fault", ["finder-extra", "merge-extra", "empty-reason"])
def test_map_locator_schema_accepts_only_locators_and_meaningful_reasons(fault):
    reports, merge, frozen = overlapping()
    if fault == "finder-extra":
        reports["haiku-finder"]["code"][0]["decision"] = "change architecture"
    elif fault == "merge-extra":
        merge["code"][0]["decision"] = "change architecture"
    else:
        reports["haiku-finder"]["code"][0]["reason"] = " "
        merge["code"][0]["origins"][0]["reason"] = " "
    with pytest.raises(module().ResearchMapError) as failure:
        module().merge_research_map(reports, merge, frozen, [], OWN)
    assert failure.value.exit_code == 1


@pytest.mark.parametrize("own", [None, "", "templates/spec.md", "../own/spec.md"])
def test_map_given_validation_requires_an_unambiguous_own_spec_context(own):
    with pytest.raises(module().ResearchMapError) as failure:
        module().validate_given_neighbours({"neighbours": []}, sources(), own)
    assert failure.value.exit_code == 2


@pytest.mark.parametrize("fault", ["empty-category", "blank-unread", "lost-origin", "changed-origin"])
def test_map_empty_categories_keep_explicit_unread_provenance(fault):
    reports, merge, frozen = overlapping()
    if fault == "empty-category":
        reports["haiku-finder"]["rules"] = []
    elif fault == "blank-unread":
        reports["haiku-finder"]["rules"] = [{"not_read": " "}]
    elif fault == "lost-origin":
        merge["rules"][0]["not_read"].pop()
    else:
        merge["rules"][0]["not_read"][0]["reason"] = "invented"
    with pytest.raises(module().ResearchMapError) as failure:
        module().merge_research_map(reports, merge, frozen, [], OWN)
    assert failure.value.exit_code == 1


def test_map_unread_categories_preserve_each_finder_reason():
    reports, merge, frozen = overlapping()
    result = module().merge_research_map(reports, merge, frozen, [], OWN)
    unread = next(row for row in result["not_read"] if row["category"] == "rules")
    assert {origin["finder"] for origin in unread["origins"]} == set(reports)
    assert all(origin["reason"] == "no locator found" for origin in unread["origins"])


@pytest.mark.parametrize("reason", [42, None, [], {}, "", "   "])
def test_finder_validation_refuses_malformed_reasons(reason):
    report = {category: [{"not_read": reason}] for category in ("code", "rules", "tests", "neighbours")}
    with pytest.raises(module().ResearchMapError):
        module().validate_locator_report(report)
    report = empty()
    report["code"] = [finder("src/app.py", "run", reason)]
    with pytest.raises(module().ResearchMapError):
        module().validate_locator_report(report)
