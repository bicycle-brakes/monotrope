"""Structured research reports retain dissent while enforcing evidence bounds."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


def module():
    import stage2_research_report

    return stage2_research_report


SOURCES = {"a.py": b"def existing():\n    return True\n"}
NEIGHBOUR = "plans/changes/peer/spec.md"


def report(*, topic=1, evidence=None):
    claim = {
        "id": "C1",
        "statement": "An existing function is present.",
        "kind": "fact",
        "evidence": ["a.py::existing"] if evidence is None else evidence,
        "confidence": "high",
        "basis": "The referenced source.",
    }
    if topic == 6:
        claim["volatile"] = False
    value = {
        "claims": [claim],
        "counter_evidence": [],
        "not_read": [],
        "neighbour_relation": "not-assessable" if topic >= 9 else "No comparison established.",
        "questions": [],
    }
    if topic == 3:
        value["class_assessment"] = {"class": "feature", "claims": ["C1"]}
    if topic == 5:
        value["neighbour_relations"] = []
        value["not_read"] = ["no packet neighbour"]
    return value


def validate(value, *, topic=1, **kwargs):
    return module().validate_research_report(
        value, run_id="run-one", topic=topic, seat="opencode-go:flash-one", sources=SOURCES, **kwargs
    )


def test_report_namespaces_claims_and_questions_without_changing_raw_report():
    value = report()
    value["questions"] = [
        {"id": "Q1", "question": "Should this behavior change?", "classification": "[DECISION]", "claims": ["C1"]}
    ]
    before = copy.deepcopy(value)
    result = validate(value)
    assert value == before
    claim = result["claims"][0]
    assert claim["id"] == "run-one/1/opencode-go:flash-one/C1" and claim["local_id"] == "C1"
    assert claim["evidence_status"] == "valid"
    assert claim["resolved"][0]["excerpt"] == SOURCES["a.py"].decode()
    assert result["questions"][0]["claims"] == [claim["id"]]
    assert result["questions"][0]["id"] == "run-one/1/opencode-go:flash-one/Q1"
    assert result["raw"] == value


def test_report_bad_citation_invalidates_whole_claim_without_dropping_it():
    value = report(evidence=["a.py::existing", "a.py::absent"])
    good = report()["claims"][0]
    good["id"] = "C2"
    value["claims"].append(good)
    value["questions"] = [
        {"id": "Q1", "question": "A decision still needed.", "classification": "[DECISION]", "claims": ["C1"]}
    ]
    result = validate(value)
    assert result["claims"][0]["evidence_status"] == "unsupported"
    assert all("excerpt" not in ref for ref in result["claims"][0]["resolved"])
    assert result["claims"][1]["evidence_status"] == "valid"
    assert result["questions"][0]["claims"] == [result["claims"][0]["id"]]


def test_report_without_any_supported_claim_fails_except_empty_neighbours():
    with pytest.raises(module().ResearchReportError, match="evidence"):
        validate(report(evidence=["a.py::absent"]))
    empty = report(topic=5)
    empty["claims"] = []
    assert validate(empty, topic=5)["claims"] == []
    empty["not_read"] = []
    with pytest.raises(module().ResearchReportError, match="neighbour"):
        validate(empty, topic=5)


def test_report_one_shared_unicode_excerpt_cap_in_citation_order():
    large = {name + ".md": ("# " + name + "\n" + "ü" * 5000).encode() for name in ("First", "Second", "Third")}
    result = module().validate_research_report(
        report(evidence=[name + ".md::" + name for name in ("First", "Second", "Third")]),
        run_id="run-one",
        topic=1,
        seat="go:model",
        sources=large,
    )
    refs = result["claims"][0]["resolved"]
    assert [ref["citation"] for ref in refs] == [name + ".md::" + name for name in ("First", "Second", "Third")]
    assert sum(len(ref["excerpt"]) for ref in refs) == 4000
    assert all(ref["truncated"] for ref in refs)
    assert refs[0]["excerpt"].startswith("# First\n") and refs[1]["excerpt"] == refs[2]["excerpt"] == ""


@pytest.mark.parametrize("citation", ["#123", "coding-harness-example", "a" * 40, "a.py:1"])
def test_report_absent_history_and_external_identifiers_are_unsupported(citation):
    with pytest.raises(module().ResearchReportError, match="evidence"):
        validate(report(topic=6, evidence=[citation]), topic=6, history={"commits": {}})


def test_report_commit_evidence_is_only_the_topic_six_packet_record():
    sha = "a" * 40
    history = {
        "commits": {
            sha: {
                "hash": sha,
                "author_utc": "2000-01-01T00:00:00Z",
                "subject": "recorded",
                "body": "bounded",
                "body_truncated": False,
                "touched_mapped_paths": ["a.py"],
            }
        }
    }
    value = report(topic=6, evidence=[sha])
    result = validate(value, topic=6, history=history)
    assert result["claims"][0]["resolved"][0]["kind"] == "commit"
    assert "recorded" in result["claims"][0]["resolved"][0]["excerpt"]
    with pytest.raises(module().ResearchReportError, match="evidence"):
        validate(report(evidence=[sha]), history=history)


def receipt(url="https://example.org/source", **changes):
    return {
        "kind": "fetch",
        "status": 200,
        "url": url,
        "final_url": url + "/final",
        "title": "Primary source",
        "retrieved": "2000-01-01T00:00:00Z",
        "excerpt": "Retrieved page text.",
        **changes,
    }


def test_report_online_claim_requires_all_own_successful_page_receipts():
    fetched = receipt()
    value = report(topic=9, evidence=[fetched["final_url"]])
    assert validate(value, topic=9, receipts=[fetched])["claims"][0]["evidence_status"] == "valid"
    for bad in (receipt(kind="search"), receipt(status=404), receipt(status=True)):
        with pytest.raises(module().ResearchReportError, match="evidence"):
            validate(value, topic=9, receipts=[bad])
    value["claims"][0]["evidence"].append("https://example.org/not-fetched")
    with pytest.raises(module().ResearchReportError, match="evidence"):
        validate(value, topic=9, receipts=[fetched])


def test_report_public_citations_cannot_attach_private_sources_or_neighbour_identities():
    with pytest.raises(module().ResearchReportError, match="evidence"):
        validate(report(topic=9), topic=9)
    value = report(topic=9, evidence=["https://example.org/source"])
    value["neighbour_relation"] = "Related to a private specification."
    with pytest.raises(module().ResearchReportError, match="neighbour"):
        validate(value, topic=9, receipts=[receipt()])


@pytest.mark.parametrize(
    "changes",
    [
        {"claims": ["C1", "C1"]},
        {"claims": ["C2"]},
        {"claims": []},
        {"classification": "guess"},
        {"id": "Q0"},
        {"answer": "fabricated"},
    ],
)
def test_report_questions_have_unique_local_links_and_no_answers(changes):
    value = report()
    value["questions"] = [
        {"id": "Q1", "question": "Need a decision.", "classification": "[DECISION]", "claims": ["C1"], **changes}
    ]
    with pytest.raises(module().ResearchReportError):
        validate(value)


@pytest.mark.parametrize("topic", [3, 6])
def test_report_topic_specific_class_and_volatile_fields_are_required(topic):
    value = report(topic=topic)
    if topic == 3:
        del value["class_assessment"]
    else:
        del value["claims"][0]["volatile"]
    with pytest.raises(module().ResearchReportError):
        validate(value, topic=topic)


def test_report_true_volatile_claim_requires_one_governance_proposal():
    value = report(topic=6)
    value["claims"][0]["volatile"] = True
    with pytest.raises(module().ResearchReportError):
        validate(value, topic=6)
    value["claims"][0]["governance"] = "runtime"
    assert validate(value, topic=6)["claims"][0]["governance"] == "runtime"


def test_report_topic_five_relations_cover_exact_neighbour_packet_and_local_claims():
    value = report(topic=5)
    value["neighbour_relations"] = [{"path": NEIGHBOUR, "relation": "contradicts", "claims": ["C1"]}]
    result = validate(value, topic=5, neighbours=[NEIGHBOUR])
    assert result["neighbour_relations"][0]["claims"] == [result["claims"][0]["id"]]
    for relation in (
        [],
        value["neighbour_relations"] * 2,
        [{"path": NEIGHBOUR, "relation": "related", "claims": ["missing"]}],
        [{"path": "plans/changes/other/spec.md", "relation": "related", "claims": ["C1"]}],
    ):
        value["neighbour_relations"] = relation
        with pytest.raises(module().ResearchReportError):
            validate(value, topic=5, neighbours=[NEIGHBOUR])


@pytest.mark.parametrize("raw", ['{"claims": [], "claims": []}', '{"claims": NaN}', "[]"])
def test_report_raw_duplicate_and_nonfinite_json_is_not_a_valid_template(raw):
    with pytest.raises(module().ResearchReportError):
        validate(raw)


def test_report_duplicate_ids_and_extra_fields_are_refused():
    value = report()
    value["claims"] *= 2
    with pytest.raises(module().ResearchReportError):
        validate(value)
    value = report()
    value["answer"] = "A model cannot decide."
    with pytest.raises(module().ResearchReportError):
        validate(value)
    value = report()
    value["claims"][0]["id"] = "C8"
    with pytest.raises(module().ResearchReportError):
        validate(value)


def test_report_raw_json_and_object_have_the_same_frozen_result():
    assert validate(json.dumps(report())) == validate(report())


def test_report_retains_online_unsupported_claim_without_any_partial_page_excerpt():
    good = receipt()
    value = report(topic=9, evidence=[good["url"], "https://example.org/missing"])
    second = copy.deepcopy(value["claims"][0])
    second.update(id="C2", evidence=[good["final_url"]])
    value["claims"].append(second)
    result = validate(value, topic=9, receipts=[good])
    assert result["claims"][0]["evidence_status"] == "unsupported"
    assert all("excerpt" not in item for item in result["claims"][0]["resolved"])
    assert result["claims"][1]["evidence_status"] == "valid"


@pytest.mark.parametrize("mutate", ["duplicate-question", "eighth-claim", "claim-verdict", "global-identity"])
def test_report_model_cannot_supply_duplicate_or_runner_owned_fields(mutate):
    value = report()
    if mutate == "duplicate-question":
        value["questions"] = [{"id": "Q1", "question": "Decide?", "classification": "[DECISION]", "claims": ["C1"]}] * 2
    elif mutate == "eighth-claim":
        value["claims"] = [{**value["claims"][0], "id": "C" + str(index)} for index in range(1, 9)]
    elif mutate == "claim-verdict":
        value["claims"][0]["evidence_status"] = "valid"
    else:
        value["seat"] = "pretend-endpoint:model"
    with pytest.raises(module().ResearchReportError):
        validate(value)


@pytest.mark.parametrize(
    "changes",
    [
        {"retrieved": "not a date"},
        {"retrieved": "2000-01-01"},
        {"excerpt": None},
        {"final_url": "https://localhost/page"},
        {"final_url": "https://user:pass@example.org/page"},
        {"final_url": "http://example.org/page"},
    ],
)
def test_report_bad_page_receipt_never_becomes_evidence(changes):
    with pytest.raises(module().ResearchReportError, match="evidence"):
        validate(report(topic=9, evidence=["https://example.org/source"]), topic=9, receipts=[receipt(**changes)])


def test_report_same_local_ids_in_two_endpoint_seats_are_distinct():
    first = validate(report())
    second = module().validate_research_report(
        report(), run_id="run-one", topic=1, seat="claude-code-plan:haiku", sources=SOURCES
    )
    assert first["claims"][0]["id"] != second["claims"][0]["id"]


@pytest.mark.parametrize("raw_json", [False, True])
def test_report_lone_surrogate_cannot_enter_a_utf8_artifact(raw_json):
    value = report()
    value["claims"][0]["statement"] = "\ud800"
    with pytest.raises(module().ResearchReportError):
        validate(json.dumps(value) if raw_json else value)


def test_report_documented_base_object_matches_the_validated_contract():
    path = Path(__file__).resolve().parents[1] / "prompts" / "research-swarm" / "report.md"
    text = path.read_text()
    example = json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])
    result = module().validate_research_report(
        example,
        run_id="example-run",
        topic=1,
        seat="go:model",
        sources={"path/to/module.py": b"def existing_symbol():\n    return True\n"},
    )
    assert result["claims"][0]["evidence_status"] == "valid"
    assert result["questions"][0]["claims"] == [result["claims"][0]["id"]]


@pytest.mark.parametrize("seat", ["unqualified", ":model", "endpoint:", "endpoint:model:ambiguous"])
def test_report_requires_one_endpoint_qualified_seat_identity(seat):
    with pytest.raises(module().ResearchReportError, match="identity"):
        module().validate_research_report(report(), run_id="run-one", topic=1, seat=seat, sources=SOURCES)


def test_report_seat_encoding_distinguishes_reserved_model_and_endpoint_characters():
    make_seat = module().research_seat_id
    assert make_seat("go", "model/version:free") == "go:model%2Fversion%3Afree"
    assert make_seat("go", "model%2Fversion:free") == "go:model%252Fversion%3Afree"
    assert make_seat("go:other", "model") == "go%3Aother:model"
    seat = make_seat("go", "model/version:free")
    result = module().validate_research_report(report(), run_id="run-one", topic=1, seat=seat, sources=SOURCES)
    assert result["claims"][0]["id"] == "run-one/1/" + seat + "/C1"
